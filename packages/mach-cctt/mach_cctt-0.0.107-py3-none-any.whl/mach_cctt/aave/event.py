from dataclasses import dataclass
from decimal import Decimal

from mach_client import Token


@dataclass
class RebalanceEvaluation:
    rates: list[tuple[Token, Decimal]]
    portfolio_balances: list[tuple[Token, Decimal]]
    portfolio_interest_rate: Decimal
    rebalance: bool


@dataclass
class Withdraw:
    amounts: list[tuple[Token, Decimal]]


@dataclass
class Supply:
    amounts: list[tuple[Token, Decimal]]

@dataclass
class LiquidityRateError:
    tokens: list[Token]
    exception: Exception


@dataclass
class WithdrawError:
    token: Token
    amount: Decimal
    exception: Exception


@dataclass
class ConvertError:
    src_token: Token
    error: object


@dataclass
class SupplyError:
    token: Token
    amount: Decimal
    exception: Exception


AaveError = LiquidityRateError | WithdrawError | ConvertError | SupplyError

AaveEvent = RebalanceEvaluation | Withdraw | Supply | AaveError
