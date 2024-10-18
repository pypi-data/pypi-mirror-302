import itertools
import re
from decimal import Decimal
from typing import Optional

import pint.testing
import pytest

from alhambra_mixes import (
    Q_,
    Component,
    EqualConcentration,
    FixedConcentration,
    FixedVolume,
    Mix,
    MultiFixedConcentration,
    MultiFixedVolume,
    Reference,
    Strand,
    VolumeError,
    WellPos,
    load_reference,
    nM,
    uM,
    ureg,
)
from alhambra_mixes.actions import ToConcentration


def test_wellpos_movement():
    "Ensure WellPos movements are correct, and fail when appropriate."

    assert WellPos("A5").next_byrow() == WellPos("A6")
    assert WellPos("A12", platesize=96).next_byrow() == WellPos("B1")
    assert WellPos("A12", platesize=96).next_bycol() == WellPos("B12")

    with pytest.raises(
        ValueError, match=r"Row I \(9\) out of bounds for plate size 96"
    ):
        WellPos("H12", platesize=96).next_byrow()

    with pytest.raises(ValueError, match="Column 13 out of bounds for plate size 96"):
        WellPos("H12", platesize=96).next_bycol()

    assert WellPos("A12", platesize=384).next_byrow() == "A13"

    assert WellPos("H14", platesize=384).next_bycol() == "I14"

    assert WellPos("A12", platesize=384) == WellPos("A12", platesize=96)

    assert WellPos("D6") == WellPos(4, 6)

    assert WellPos("D6") == "D6"

    assert str(WellPos("D6")) == "D6"

    assert repr(WellPos("D8")) == 'WellPos("D8")'

    assert WellPos("C8").key_byrow() == (3, 8)

    assert WellPos("C8").key_bycol() == (8, 3)

    assert WellPos("D8") == WellPos(WellPos("D8"))


def test_invalid_wellrefs():
    with pytest.raises(ValueError):
        WellPos("A14", platesize=96)

    with pytest.raises(ValueError):
        WellPos("Q14", platesize=384)

    with pytest.raises(ValueError):
        WellPos("H25", platesize=384)

    with pytest.raises(ValueError, match="Plate size 1536 not supported"):
        WellPos("A1", platesize=1536)

    assert WellPos("D8") != str

    with pytest.raises(TypeError):
        WellPos(5.3)

    with pytest.raises(ValueError):
        WellPos("i123nvalid string")


def _itertools_pairwise(iterable):  # FIXME: in 3.10
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def test_all_wellref_96():
    allbyrow96 = [f"{r}{c}" for r in "ABCDEFGH" for c in range(1, 13)]
    for x, y in _itertools_pairwise(allbyrow96):
        assert WellPos(x, platesize=96).next_byrow() == y

    allbyrow96 = [f"{r}{c}" for c in range(1, 13) for r in "ABCDEFGH"]
    for x, y in _itertools_pairwise(allbyrow96):
        assert WellPos(x, platesize=96).next_bycol() == y


def test_component():
    assert Component("test1") != Component("test2")

    assert Component("test3") == Component("test3")

    assert Component("A", 1 * uM) == Component("A", 1000 * nM)

    assert Component("A", 1 * uM) != Component("A", 1002 * nM)

    assert Component("A") != Strand("A")

    assert Component("A") != 5


def test_component_allcomps():
    ac = Component("A", 1 * uM).all_components()

    assert len(ac) == 1
    assert ac.loc["A", "component"] == Component("A", 1 * uM)
    assert ac.loc["A", "concentration_nM"] == Decimal("1000.0")


@pytest.fixture
def reference():
    return Reference.from_csv("tests/data/test_reference.csv")


def test_reference_saveload(
    tmp_path_factory: pytest.TempPathFactory, reference: Reference
):
    sf = tmp_path_factory.mktemp("exp") / "test.csv"

    r = load_reference("tests/data/test_reference.csv")

    assert r == reference

    r.to_csv(sf)

    r2 = Reference.from_csv(sf)

    assert r == r2

    assert r == r2.df


def test_component_with_reference(reference: Reference):
    c = Component("comp1")
    d = c.with_reference(reference)

    assert c != d
    assert d.concentration, ureg("1000.0 nM")

    with pytest.raises(ValueError):
        Component("comp1", ureg("150.0 nM")).with_reference(reference)


def test_strand_with_reference(reference: Reference):
    c = Strand("strand1")
    d = c.with_reference(reference)

    assert c != d
    assert d.concentration == ureg("1000.0 nM")
    assert d.sequence == "AGAACC"

    with pytest.raises(ValueError):
        Strand("strand1", ureg("150.0 nM")).with_reference(reference)

    with pytest.raises(ValueError):
        Strand("strand1", sequence="AGCTG").with_reference(reference)


def test_with_reference_get_first(
    reference: Reference, caplog: pytest.LogCaptureFixture
):
    s = Strand("strand3").with_reference(reference)

    r1 = caplog.records[0]
    assert re.match(r"Strand %s has more than one location", r1.msg)
    assert r1.args == (
        s.name,
        [("P 2", "D7"), ("P 2", "D5"), ("P 3", "D7"), ("P 4", "D7")],
    )

    assert s == Strand("strand3", Q_(1000, nM), sequence="GGTG", plate="P 2", well="D7")


def test_with_reference_constraints_match_plate(reference: Reference, caplog):
    s = Strand("strand3", plate="P 3").with_reference(reference)
    assert s == Strand("strand3", Q_(2000, nM), sequence="GGTG", plate="P 3", well="D7")

    c = Component("strand3", plate="P 3").with_reference(reference)
    assert c == Component("strand3", Q_(2000, nM), plate="P 3", well="D7")


def test_with_reference_constraints_match_well(reference: Reference, caplog):
    s = Strand("strand3", well="D5").with_reference(reference)
    assert s == Strand("strand3", Q_(1000, nM), sequence="GGTG", plate="P 2", well="D5")

    c = Component("strand3", well="D5").with_reference(reference)
    assert c == Component("strand3", Q_(1000, nM), plate="P 2", well="D5")


def test_with_reference_constraints_match_seq(reference: Reference, caplog):
    s = Strand("strand3", sequence="GGTGAGG").with_reference(reference)
    assert s == Strand(
        "strand3", Q_(2000, nM), sequence="GGTG AGG", plate="P 4", well="D7"
    )


def test_a_mix(reference: Reference):
    c1 = Component("comp1")
    s1 = Strand("strand1")
    s2 = Strand("strand2")
    s3 = Strand("strand3", ureg("1000 nM"), sequence="GGTG")

    m = Mix(
        [
            MultiFixedVolume([s1, s2, s3], ureg("10 uL"), compact_display=True),
            FixedConcentration(c1, "100 nM"),
            FixedVolume(s3, ureg("10 uL")),
        ],
        name="test",
        test_tube_name="tm1",
        fixed_total_volume=ureg("50 uL"),
        fixed_concentration="strand3",
    ).with_reference(reference)

    assert m.buffer_volume == ureg("5 uL")
    assert m.concentration == ureg("400 nM")

    mdt = m._repr_markdown_().splitlines()

    assert (
        re.match(
            r"Table: Mix: test, Conc: 400.00 nM, Total Vol: 50.00 µl, Test tube name: tm1",
            mdt[0],
        )
        is not None
    )

    ml = m.mixlines(tablefmt="pipe")

    assert sum(l.total_tx_vol for l in ml if not l.fake) == m.total_volume

    for line in ml:
        if line.fake:
            continue
        if line.each_tx_vol:
            assert line.number * line.each_tx_vol == line.total_tx_vol


def test_multifixedconc_min_volume(reference: Reference):
    s1 = Strand("strand1", "400 nM")
    s2 = Strand("strand2", "200 nM")

    m = Mix(
        [FixedConcentration([s1, s2], "50 nM", min_volume="20 uL")],
        name="test",
        fixed_total_volume="100 uL",
    )

    with pytest.raises(VolumeError):
        m.table(raise_failed_validation=True)

    m.fixed_total_volume = "200 uL"  # type: ignore  # Mypy doesn't understand on_setattr

    m.table()


def test_mix_min_volume(reference: Reference):
    s1 = Strand("strand1", "100 nM")

    # should need 10 uL in 100 uL total volume to dilute from 100 nM to 10 nM,
    # so set min_volume to 20 uL to trigger error
    m = Mix(
        [FixedConcentration(s1, "10 nM")],
        name="test",
        fixed_total_volume="100 uL",
        min_volume="20 uL",
    )

    with pytest.raises(VolumeError):
        m.table(raise_failed_validation=True)

    # should need 20 uL in 200 uL total volume to dilute from 100 nM to 10 nM,
    # so should work with min_volume=20 uL
    m.fixed_total_volume = "200 uL"  # type: ignore  # Mypy doesn't understand on_setattr

    m.table()


def test_non_plates():
    s1 = Strand("s1", "200 nM", plate="tube")

    s2 = Strand("s2", "200 nM", plate="tube")

    s3 = Strand("s3", "400 nM", plate="tube")

    s4 = Strand("s4", "400 nM", plate="a different tube")

    m = Mix(
        [EqualConcentration([s1, s2, s3, s4], "1 uL", method="min_volume")],
        "test",
        min_volume="0 uL",
    )

    m.table()

    ml = m.mixlines(tablefmt="pipe")

    assert len(ml) == 3


def test_fixedvolume_equal_conc_deprecation():
    s1 = Strand("s1", "200 nM", plate="tube")

    s2 = Strand("s2", "200 nM", plate="tube")

    s3 = Strand("s3", "400 nM", plate="tube")

    s4 = Strand("s4", "400 nM", plate="a different tube")

    with pytest.warns(
        DeprecationWarning,
        match=r"The equal_conc parameter for FixedVolume is no longer supported.",
    ):
        a = FixedVolume([s1, s2, s3, s4], "1 uL", equal_conc="min_volume")  # type: ignore

    b = EqualConcentration([s1, s2, s3, s4], "1 uL", method="min_volume")

    assert a == b


def test_intermediate_mix_sufficient_volume():
    s1 = Strand("s1", "100 uM", plate="plate1", well="A1")
    s2 = Strand("s2", "100 uM", plate="plate1", well="A2")
    s3 = Strand("s3", "100 uM", plate="plate1", well="B3")
    s4 = Strand("s4", "100 uM", plate="plate1", well="B4")

    i1_mix = Mix(
        actions=[
            MultiFixedConcentration([s1, s2], fixed_concentration="10 uM"),
        ],
        name="intermediate mix 1",
        fixed_total_volume="15uL",
    )
    i2_mix = Mix(
        actions=[
            MultiFixedConcentration([s3, s4], fixed_concentration="5 uM"),
        ],
        name="intermediate mix 2",
        fixed_total_volume="15uL",
    )

    # 15 is enough for i1_mix but not i2_mix, which requires 20 uL in final_mix
    final_mix = Mix(
        actions=[
            MultiFixedConcentration([i1_mix, i2_mix], fixed_concentration="1 uM"),
        ],
        name="final mix",
        fixed_total_volume="100uL",
    )

    with pytest.raises(VolumeError):
        final_mix.table(raise_failed_validation=True)


def test_toconcentration():
    ca = Component("A", "1 µM")
    cb = Component("B", "1 µM")
    cc = Component("C", "1 µM")

    ma = Mix(
        [FixedConcentration(ca, "100 nM"), FixedVolume(cb, "11 µL")],
        "imix",
        fixed_total_volume="100 µL",
    )

    tca = ToConcentration(ca, "150 nM")
    tcb = ToConcentration([ca, cb], "150 nM")

    assert tcb.dest_concentrations(
        ureg("100 µL"),
        [FixedConcentration([ca], "50 nM"), FixedConcentration([cc], "55 nM")],
    ) == [ureg("100 nM"), ureg("150 nM")]

    assert tcb.dest_concentrations(
        ureg("100 µL"), [FixedVolume([ma], "50 µL"), FixedConcentration(ca, "10 nM")]
    ) == [ureg("90 nM"), ureg("95 nM")]

    mix = Mix(
        [
            ToConcentration(ca, "150 nM"),
            ToConcentration([cb, cc], "140 nM"),
            FixedConcentration(ma, "50 nM"),
            FixedVolume(cc, "1 µL"),
        ],
        "testmix",
        fixed_total_volume="100 µL",
    )

    ac = mix.all_components()

    assert ac.loc["A", "concentration_nM"] == 150
    assert ac.loc["B", "concentration_nM"] == 140
    assert ac.loc["C", "concentration_nM"] == 140

    ml = mix.mixlines("pipe")

    print(mix.table())

    assert [m.dest_conc for m in ml] == [
        Q_(x, nM) for x in ["100", "85", "130", "50", "10"]
    ] + [None]


def test_combine_plate_actions():
    from alhambra_mixes import Mix, MultiFixedConcentration, Strand

    s1 = Strand("s1", "40 uM", plate="plate1", well="A1")
    s2 = Strand("s2", "40 uM", plate="plate1", well="A2")
    s3 = Strand("s3", "40 uM", plate="plate2", well="B1")
    s4 = Strand("s4", "40 uM", plate="plate2", well="B2")
    mix = Mix(
        actions=[
            MultiFixedConcentration([s1, s3], fixed_concentration="10 uM"),
            MultiFixedConcentration([s2, s4], fixed_concentration="10 uM"),
        ],
        name="test",
        fixed_total_volume="40uL",
        min_volume="0 uL",
    )

    combine_plate_actions = True
    pms = mix.plate_maps(combine_plate_actions=combine_plate_actions)
    assert len(pms) == 2

    assert len(pms[0].well_to_strand_name) == 2
    assert len(pms[1].well_to_strand_name) == 2
    assert "A1" in pms[0].well_to_strand_name
    assert "A2" in pms[0].well_to_strand_name
    assert "B1" in pms[1].well_to_strand_name
    assert "B2" in pms[1].well_to_strand_name
    assert pms[0].well_to_strand_name["A1"] == "s1"
    assert pms[0].well_to_strand_name["A2"] == "s2"
    assert pms[1].well_to_strand_name["B1"] == "s3"
    assert pms[1].well_to_strand_name["B2"] == "s4"


def test_combine_plate_actions_false():
    # this is sort of a "control" for the previous test; make sure we can reproduce old behavior
    from alhambra_mixes import Mix, MultiFixedConcentration, Strand

    s1 = Strand("s1", "40 uM", plate="plate1", well="A1")
    s2 = Strand("s2", "40 uM", plate="plate1", well="A2")
    s3 = Strand("s3", "40 uM", plate="plate2", well="B1")
    s4 = Strand("s4", "40 uM", plate="plate2", well="B2")
    mix = Mix(
        actions=[
            MultiFixedConcentration([s1, s3], fixed_concentration="10 uM"),
            MultiFixedConcentration([s2, s4], fixed_concentration="10 uM"),
        ],
        name="test",
        fixed_total_volume="40uL",
        min_volume="0 uL",
    )

    combine_plate_actions = False
    pms = mix.plate_maps(combine_plate_actions=combine_plate_actions)
    assert len(pms) == 4

    assert len(pms[0].well_to_strand_name) == 1
    assert len(pms[1].well_to_strand_name) == 1
    assert "A1" in pms[0].well_to_strand_name
    assert "B1" in pms[1].well_to_strand_name
    assert "A2" in pms[2].well_to_strand_name
    assert "B2" in pms[3].well_to_strand_name
    assert pms[0].well_to_strand_name["A1"] == "s1"
    assert pms[1].well_to_strand_name["B1"] == "s3"
    assert pms[2].well_to_strand_name["A2"] == "s2"
    assert pms[3].well_to_strand_name["B2"] == "s4"


def assert_close(
    actual: Decimal,
    expected: Decimal,
    rtol: Decimal = Decimal(1e-7),
    atol: Decimal = Decimal(0),
    msg: Optional[str] = None,
) -> None:
    # This helps with comparing Decimal quantities, which cannot be multiplied by floats, which is
    # what happens with the default rtol parameter of pint.testing.assert_allclose.
    pint.testing.assert_allclose(actual, expected, rtol, atol, msg) # type: ignore


def test_split_mix():
    from alhambra_mixes import FixedConcentration, FixedVolume, Mix, Strand, split_mix

    staples = [Strand(f"stap{i}", concentration="1uM") for i in range(10)]
    staple_mix = Mix(
        actions=[FixedConcentration(components=staples, fixed_concentration="100 nM")],
        name="staple mix",
    )
    m13 = Strand("m13 100nM", concentration="100 nM")
    buffer_10x = Component(name="10x buffer", concentration="100 mM")
    mix = Mix(
        actions=[
            FixedVolume(components=[buffer_10x], fixed_volume="10 uL"),
            FixedConcentration(components=[m13], fixed_concentration="1 nM"),
            FixedConcentration(components=[staple_mix], fixed_concentration="10 nM"),
        ],
        name="mm",
        fixed_total_volume="100 uL",
    )
    sm = split_mix(mix=mix, num_tubes=5, excess=0)

    assert_close(sm.buffer_volume, ureg("395 uL"))

    mixlines = sm.mixlines()
    assert len(mixlines) == 4

    buffer_10x_mixline, m13_mixline, staple_mixline, buffer_mixline = mixlines

    assert_close(buffer_10x_mixline.total_tx_vol, ureg("50 uL"))
    assert_close(m13_mixline.total_tx_vol, ureg("5 uL"))
    assert_close(staple_mixline.total_tx_vol, ureg("50 uL"))
    assert_close(buffer_mixline.total_tx_vol, ureg("395 uL"))


def test_split_mix_with_excess():
    from alhambra_mixes import FixedConcentration, FixedVolume, Mix, Strand, split_mix

    staples = [Strand(f"stap{i}", concentration="1uM") for i in range(10)]
    staple_mix = Mix(
        actions=[FixedConcentration(components=staples, fixed_concentration="100 nM")],
        name="staple mix",
    )
    m13 = Strand("m13 100nM", concentration="100 nM")
    buffer_10x = Component(name="10x buffer", concentration="100 mM")
    mix = Mix(
        actions=[
            FixedVolume(components=[buffer_10x], fixed_volume="10 uL"),
            FixedConcentration(components=[m13], fixed_concentration="1 nM"),
            FixedConcentration(components=[staple_mix], fixed_concentration="10 nM"),
        ],
        name="mm",
        fixed_total_volume="100 uL",
    )
    sm = split_mix(mix=mix, num_tubes=5, excess=0.1)

    assert_close(sm.buffer_volume, ureg("434.50 uL"))

    mixlines = sm.mixlines()
    assert len(mixlines) == 4

    buffer_10x_mixline, m13_mixline, staple_mixline, buffer_mixline = mixlines

    assert_close(buffer_10x_mixline.total_tx_vol, ureg("55 uL"))
    assert_close(m13_mixline.total_tx_vol, ureg("5.5 uL"))
    assert_close(staple_mixline.total_tx_vol, ureg("55 uL"))
    assert_close(buffer_mixline.total_tx_vol, ureg("434.50 uL"))


@pytest.fixture
def master_mix_fixture():
    from alhambra_mixes import FixedConcentration, Mix, Strand

    s1 = Strand("s1", concentration="100 nM")
    s2 = Strand("s2", concentration="100 nM")
    s3 = Strand("s3", concentration="100 nM")
    s4 = Strand("s4", concentration="100 nM")
    s5 = Strand("s5", concentration="100 nM")
    s6 = Strand("s6", concentration="100 nM")
    s7 = Strand("s7", concentration="100 nM")
    s8 = Strand("s8", concentration="100 nM")
    mixes = [
        Mix(
            actions=[
                FixedConcentration(components=[s1, s2], fixed_concentration="10 nM"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s7], fixed_concentration="10 nM"),
            ],
            name="mix 0",
            fixed_total_volume="100 uL",
        ),
        Mix(
            actions=[
                FixedConcentration(components=[s1, s2], fixed_concentration="10 nM"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s8], fixed_concentration="10 nM"),
            ],
            name="mix 1",
            fixed_total_volume="100 uL",
        ),
    ]
    return mixes


def test_master_mix(master_mix_fixture):
    from alhambra_mixes import master_mix

    mixes = master_mix_fixture

    mm, final_mixes = master_mix(mixes=mixes, name="master mix", excess=0)

    assert mm.total_volume == ureg("180 uL")

    mm_mixlines = mm.mixlines()
    assert len(mm_mixlines) == 4  # 3 mixes shared plus buffer

    s12_ml, s34_ml, s56_ml, buffer_ml = mm_mixlines

    # print(mm.instructions() + '\n')
    # for mix in final_mixes:
    #     print(mix.instructions() + '\n')

    assert_close(s12_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s34_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s56_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s12_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s34_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s56_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s12_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(s34_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(s56_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(buffer_ml.each_tx_vol, ureg("60 uL"))

    assert len(final_mixes) == 2
    for i, mix in enumerate(final_mixes):
        assert mix.name == f"mix {i}"

        mixlines = mix.mixlines()
        assert len(mixlines) == 3
        mm_ml, strand_ml, buf_ml = mixlines

        assert_close(mm_ml.each_tx_vol, ureg("90 uL"))
        assert_close(strand_ml.each_tx_vol, ureg("10 uL"))
        assert_close(buf_ml.each_tx_vol, ureg("0 uL"))

        assert_close(strand_ml.total_tx_vol, ureg("10 uL"))

        assert_close(mm_ml.dest_conc, ureg("10 nM"))
        assert_close(strand_ml.dest_conc, ureg("10 nM"))

        strand_name = "s7" if i == 0 else "s8"
        assert len(strand_ml.names) == 1
        assert strand_ml.names[0] == strand_name


def test_master_mix_different_buffer_volumes():
    from alhambra_mixes import master_mix

    s1 = Component("s1", concentration="100 nM")
    s2 = Component("s2", concentration="100 nM")
    s3 = Component("s3", concentration="100 nM")
    s4 = Component("s4", concentration="100 nM")
    s5 = Component("s5", concentration="100 nM")
    s6 = Strand("s6", concentration="100 nM")
    s7 = Strand("s7", concentration="100 nM")
    s8 = Strand("s8", concentration="100 nM")

    mixes = [
        Mix(
            actions=[
                FixedConcentration(components=[s1, s2], fixed_concentration="10 nM"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
            ],
            name="mix 0",
            fixed_total_volume="100 uL",
        ),
        Mix(
            actions=[
                FixedConcentration(components=[s1, s2], fixed_concentration="10 nM"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s8], fixed_concentration="10 nM"),
            ],
            name="mix 1",
            fixed_total_volume="100 uL",
        ),
        Mix(
            actions=[
                FixedConcentration(components=[s1, s2], fixed_concentration="10 nM"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s7], fixed_concentration="10 nM"),
                FixedConcentration(components=[s8], fixed_concentration="20 nM"),
            ],
            name="mix 1",
            fixed_total_volume="100 uL",
        ),
    ]
    mm, final_mixes = master_mix(mixes=mixes, name="master mix")

    mm.validate(tablefmt="pipe", raise_errors=True)

    for mix in final_mixes:
        assert mix.total_volume == ureg("100 µL")
        mix.validate(tablefmt="pipe", raise_errors=True)


def test_master_mix_exclude_shared_components(master_mix_fixture):
    from alhambra_mixes import master_mix

    mixes = master_mix_fixture

    mm, final_mixes = master_mix(
        mixes=mixes, name="master mix", excess=0, exclude_shared_components=["s5"]
    )
    # now should only have [s1,s2] and [s3,s4] as shared components, with [s5,s6] "unique" though
    # appearing in both

    assert mm.total_volume == ureg("140 uL")

    mm_mixlines = mm.mixlines()
    assert len(mm_mixlines) == 3  # 2 mixes shared plus buffer

    s12_ml, s34_ml, buffer_ml = mm_mixlines

    # print(mm.instructions() + "\n")
    # for mix in final_mixes:
    #     print(mix.instructions() + "\n")

    assert_close(s12_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s34_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s12_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s34_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s12_ml.dest_conc, ureg("14.29 nM"), atol=Decimal(0.01))
    assert_close(s34_ml.dest_conc, ureg("14.29 nM"), atol=Decimal(0.01))
    assert_close(buffer_ml.each_tx_vol, ureg("60 uL"))

    assert len(final_mixes) == 2
    for i, mix in enumerate(final_mixes):
        assert mix.name == f"mix {i}"

        mixlines = mix.mixlines()
        assert len(mixlines) == 4
        mm_ml, s56_ml, strand_ml, buf_ml = mixlines

        assert_close(mm_ml.each_tx_vol, ureg("70 uL"))
        assert_close(s56_ml.each_tx_vol, ureg("10 uL"))
        assert_close(strand_ml.each_tx_vol, ureg("10 uL"))
        assert_close(buf_ml.each_tx_vol, ureg("0 uL"))

        assert_close(s56_ml.total_tx_vol, ureg("20 uL"))
        assert_close(strand_ml.total_tx_vol, ureg("10 uL"))

        assert_close(mm_ml.dest_conc, ureg("10 nM"))
        assert_close(s56_ml.dest_conc, ureg("10 nM"))
        assert_close(strand_ml.dest_conc, ureg("10 nM"))

        strand_name = "s7" if i == 0 else "s8"
        assert len(strand_ml.names) == 1
        assert strand_ml.names[0] == strand_name


def test_master_mix_with_FixedVolume_action(master_mix_fixture):
    from alhambra_mixes import FixedConcentration, FixedVolume, Mix, Strand, master_mix

    s1 = Strand("s1", concentration="100 nM")
    s2 = Strand("s2", concentration="100 nM")
    s3 = Strand("s3", concentration="100 nM")
    s4 = Strand("s4", concentration="100 nM")
    s5 = Strand("s5", concentration="100 nM")
    s6 = Strand("s6", concentration="100 nM")
    s7 = Strand("s7", concentration="100 nM")
    s8 = Strand("s8", concentration="100 nM")
    mixes = [
        Mix(
            actions=[
                FixedVolume(components=[s1, s2], fixed_volume="10 uL"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s7], fixed_concentration="10 nM"),
            ],
            name="mix 0",
            fixed_total_volume="100 uL",
        ),
        Mix(
            actions=[
                FixedVolume(components=[s1, s2], fixed_volume="10 uL"),
                FixedConcentration(components=[s3, s4], fixed_concentration="10 nM"),
                FixedConcentration(components=[s5, s6], fixed_concentration="10 nM"),
                FixedConcentration(components=[s8], fixed_concentration="10 nM"),
            ],
            name="mix 1",
            fixed_total_volume="100 uL",
        ),
    ]

    mm, final_mixes = master_mix(mixes=mixes, name="master mix", excess=0)

    assert mm.total_volume == ureg("180 uL")

    mm_mixlines = mm.mixlines()
    assert len(mm_mixlines) == 4  # 3 mixes shared plus buffer

    s12_ml, s34_ml, s56_ml, buffer_ml = mm_mixlines

    # print(mm.instructions() + '\n')
    # for mix in final_mixes:
    #     print(mix.instructions() + '\n')

    assert_close(s12_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s34_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s56_ml.each_tx_vol, ureg("20 uL"))
    assert_close(s12_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s34_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s56_ml.total_tx_vol, ureg("40 uL"))
    assert_close(s12_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(s34_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(s56_ml.dest_conc, ureg("11.11 nM"), atol=Decimal(0.01))
    assert_close(buffer_ml.each_tx_vol, ureg("60 uL"))

    assert len(final_mixes) == 2
    for i, mix in enumerate(final_mixes):
        assert mix.name == f"mix {i}"

        mixlines = mix.mixlines()
        assert len(mixlines) == 3
        mm_ml, strand_ml, buf_ml = mixlines

        assert_close(mm_ml.each_tx_vol, ureg("90 uL"))
        assert_close(strand_ml.each_tx_vol, ureg("10 uL"))
        assert_close(buf_ml.each_tx_vol, ureg("0 uL"))

        assert_close(strand_ml.total_tx_vol, ureg("10 uL"))

        assert_close(mm_ml.dest_conc, ureg("10 nM"))
        assert_close(strand_ml.dest_conc, ureg("10 nM"))

        strand_name = "s7" if i == 0 else "s8"
        assert len(strand_ml.names) == 1
        assert strand_ml.names[0] == strand_name
