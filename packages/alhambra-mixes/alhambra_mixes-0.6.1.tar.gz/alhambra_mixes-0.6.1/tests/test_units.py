from decimal import Decimal

import pytest

from alhambra_mixes.units import (
    Q_,
    _parse_conc_optional,
    _parse_conc_required,
    _parse_vol_optional,
    _parse_vol_optional_none_zero,
    _parse_vol_required,
    ureg,
)


def test_ensure_decimal_quantity():
    assert isinstance(ureg.Quantity("1.0 nM").m, Decimal)
    assert isinstance(Q_("1.0 nM").m, Decimal)
    assert isinstance(Q_(1.0, "nM").m, Decimal)
    assert isinstance(Q_("1.0", "nM").m, Decimal)
    # assert isinstance(Q_(Fraction(1,2), "nM").m, Decimal)
    # with pytest.raises(AssertionError):
    #     assert isinstance(pint.Quantity("1.0 nM").m, Decimal)


@pytest.mark.parametrize(
    ["func", "unit"],
    zip(
        [
            _parse_conc_optional,
            _parse_conc_required,
            _parse_vol_optional,
            _parse_vol_optional_none_zero,
            _parse_vol_required,
        ],
        ["nM", "nM", "uL", "uL", "uL"],
    ),
)
def test_parsers_return_decimal(func, unit):
    assert isinstance(func("1.0 " + unit).m, Decimal)
    # assert isinstance(func(pint.Quantity("1.0 " + unit)).m, Decimal)


@pytest.mark.parametrize(
    ["func", "unit"],
    zip(
        [
            _parse_conc_optional,
            _parse_conc_required,
            _parse_vol_optional,
            _parse_vol_optional_none_zero,
            _parse_vol_required,
        ],
        ["m^2", "nL", "C", "nM", "cm^2"],
    ),
)
def test_parsers_wrong_unit(func, unit):
    with pytest.raises(ValueError, match=".*not a valid quantity here.*"):
        func("1.0 " + unit)
    # with pytest.raises(ValueError, match=".*not a valid quantity here.*"):
    #     func(pint.Quantity("1.0 " + unit))
