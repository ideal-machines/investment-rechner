from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class YearResult:
    year: int
    contributed: float
    value: float


def monthly_rate(annual_percent: float) -> float:
    """Convert an effective annual return into an equivalent monthly rate."""
    if annual_percent <= -100:
        raise ValueError("Die Rendite muss größer als -100 % sein.")
    return (1 + annual_percent / 100) ** (1 / 12) - 1


def simulate(
    initial_capital: float,
    monthly_saving: float,
    annual_saving_increase_percent: float,
    annual_return_percent: float,
    years: int,
) -> list[YearResult]:
    """Simulate monthly deposits made at the end of each month."""
    if initial_capital < 0 or monthly_saving < 0:
        raise ValueError("Kapital und Sparrate dürfen nicht negativ sein.")
    if years < 1:
        raise ValueError("Der Anlagehorizont muss mindestens ein Jahr betragen.")
    if annual_saving_increase_percent <= -100:
        raise ValueError("Die Steigerung der Sparrate muss größer als -100 % sein.")

    balance = float(initial_capital)
    contributed = float(initial_capital)
    current_monthly_saving = float(monthly_saving)
    rate = monthly_rate(annual_return_percent)
    results = [YearResult(0, contributed, balance)]

    for year in range(1, years + 1):
        for _ in range(12):
            balance *= 1 + rate
            balance += current_monthly_saving
            contributed += current_monthly_saving
        results.append(YearResult(year, contributed, balance))
        current_monthly_saving *= 1 + annual_saving_increase_percent / 100

    return results
