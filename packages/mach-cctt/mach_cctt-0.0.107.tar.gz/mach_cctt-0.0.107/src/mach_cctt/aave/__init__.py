import asyncio
from decimal import Decimal
from pprint import pformat
from typing import AsyncGenerator, Sequence

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from mach_client import ChainId, Token, client, utility

from .. import config, mach
from ..mach.destination_policy import TokenIteratorPolicy
from ..log import Logger
from ..mach.event import EmptySourceBalance, Trade
from . import atoken
from .event import *
from .supply import supply
from . import valid_tokens
from .withdraw import withdraw


scaling_factor = 10**27


async def get_liquidity_rate(token: Token) -> Decimal:
    asset_info = client.deployments[token.chain.id]["assets"][token.symbol]

    w3 = await utility.make_w3(token.chain)

    aave_pool_address = config.aave_pool_addresses[token.chain.id]
    pool_contract = w3.eth.contract(
        address=aave_pool_address,  # type: ignore
        abi=config.aave_pool_abi(token.chain.id),
    )

    reserve_data = await pool_contract.functions.getReserveData(
        asset_info["address"]
    ).call()

    return Decimal(reserve_data[2]) / scaling_factor


async def get_liquidity_rates(
    tokens: Sequence[Token],
) -> list[tuple[Token, Decimal]]:
    liquidity_rates = await asyncio.gather(
        *(get_liquidity_rate(token) for token in tokens)
    )

    result = list(zip(tokens, liquidity_rates))
    result.sort(key=lambda x: x[1], reverse=True)

    return result


async def run(
    *,
    account: LocalAccount,
    logger: Logger,
) -> AsyncGenerator[AaveEvent, None]:
    chains = client.chains - frozenset(
        (ChainId.AVALANCHE_C_CHAIN, ChainId.BSC, ChainId.POLYGON)
    )
    symbols = frozenset(("USDC", "USDT"))
    tokens = await valid_tokens.get_valid_aave_tokens(chains, symbols)

    logger.info(f"Tokens:")
    logger.info(pformat(tokens))

    while True:

        rebalance = False

        # Inner loop determines when to rebalance portfolio
        while not rebalance:
            try:
                token_rates = await get_liquidity_rates(tokens)
            except Exception as e:
                logger.critical(
                    "An exception was thrown while fetching liquidity rates from Aave:"
                )
                logger.exception(e)
                yield LiquidityRateError(tokens, e)
                continue

            token_rate_map = dict(token_rates)

            logger.info("Liquidity rates:")
            logger.info(pformat(token_rates))

            portfolio_balances = await asyncio.gather(*[
                atoken.get_token_balance(
                    token,
                    account.address
                )
                for token in tokens
            ])

            portfolio_balance_pairs = list(zip(tokens, portfolio_balances))

            portfolio_balance = sum(portfolio_balances)

            portfolio_interest_rate = sum(
                balance * token_rate_map[token] / portfolio_balance
                for token, balance in portfolio_balance_pairs
            )

            logger.info(f"Portfolio interest rate: {portfolio_interest_rate}")

            rebalance = token_rates[0][1] - \
                portfolio_interest_rate > config.aave_rebalance_threshold

            yield RebalanceEvaluation(
                token_rates,
                portfolio_balance_pairs,
                Decimal(portfolio_interest_rate),
                rebalance
            )

            if not rebalance:
                logger.info("Not rebalancing portfolio")
                await asyncio.sleep(config.aave_supply_duration)

        logger.info("Rebalancing portfolio")

        logger.info(f"Withdrawing funds from Aave")

        withdrawn = []

        for token in tokens:
            amount, exception = await withdraw(token, account, logger)

            if exception:
                logger.critical(
                    f"An exception was thrown while withdrawing {
                        token} from Aave:"
                )
                logger.exception(exception)
                yield WithdrawError(
                    token,
                    Decimal(amount) / 10 ** token.decimals,
                    exception
                )
            elif amount <= 0:
                continue

            withdrawn.append((token, amount / 10**token.decimals))

        yield Withdraw(withdrawn)

        logger.info(f"Swapping funds in wallet")

        for src_token in filter(lambda token: token != token_rates[0][0], tokens):
            higher_rate_tokens = [
                dest_token for dest_token, rate in token_rates
                # Only swap to higher interest rate tokens
                if rate > token_rate_map[src_token]
            ]

            # If we're already in the highest interest rate pool, there's no need to swap
            if not higher_rate_tokens:
                continue

            destination_policy = TokenIteratorPolicy(
                higher_rate_tokens.__iter__())

            runner = mach.run(
                src_token=src_token,
                destination_policy=destination_policy,
                account=account,
                logger=logger,
            )

            try:
                async for event in runner:
                    # Only 2 successful cases are expected: either the trade goes through, or we never had any of the source token in the first place
                    if isinstance(event, (Trade, EmptySourceBalance)):
                        break

                    logger.error(
                        f"Unexpected event while swapping {token}:"
                    )
                    logger.error(pformat(event))

                    yield ConvertError(token, event)

            except Exception as e:
                logger.critical(
                    f"An exception was thrown while swapping {token}:"
                )
                logger.exception(e)
                yield ConvertError(token, e)

        supplied = []

        for token in tokens:
            amount, exception = await supply(token, account, logger)

            if exception:
                logger.critical(
                    f"An exception was thrown while supplying {token} to Aave:"
                )
                logger.exception(exception)
                yield SupplyError(token, amount / 10**token.decimals, e)
            elif amount <= 0:
                continue

            supplied.append((token, amount / 10**token.decimals))

        yield Supply(supplied)

        logger.info("Sleeping...")
        await asyncio.sleep(config.aave_supply_duration)
