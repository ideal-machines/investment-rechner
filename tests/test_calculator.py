import pytest

from calculator import monthly_rate, simulate


def test_monthly_rate_compounds_to_annual_rate():
    rate = monthly_rate(7)
    assert (1 + rate) ** 12 == pytest.approx(1.07)


def test_zero_return_is_contributions_only():
    rows = simulate(1_000, 100, 0, 0, 2)
    assert rows[-1].contributed == pytest.approx(3_400)
    assert rows[-1].value == pytest.approx(3_400)


def test_saving_rate_increases_after_each_year():
    rows = simulate(0, 100, 10, 0, 2)
    assert rows[1].value == pytest.approx(1_200)
    assert rows[2].value == pytest.approx(2_520)


def test_negative_capital_is_rejected():
    with pytest.raises(ValueError):
        simulate(-1, 100, 0, 5, 10)
