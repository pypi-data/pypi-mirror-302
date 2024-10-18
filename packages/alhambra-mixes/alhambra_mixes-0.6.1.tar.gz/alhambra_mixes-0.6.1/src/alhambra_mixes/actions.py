from __future__ import annotations

import math
from abc import ABCMeta, abstractmethod
from math import isnan
from typing import TYPE_CHECKING, Any, Literal, Sequence, TypeVar, cast
from warnings import warn

import attrs
import pandas as pd

from .components import AbstractComponent, _empty_components, _maybesequence_comps
from .dictstructure import _STRUCTURE_CLASSES, _structure, _unstructure
from .locations import WellPos, mixgaps
from .printing import MixLine, TableFormat
from .units import _parse_vol_optional_none_zero

import polars as pl

if TYPE_CHECKING:  # pragma: no cover
    from .experiments import Experiment
    from .references import Reference

from .units import *
from .units import (
    Q_,
    Decimal,
    DecimalQuantity,
    VolumeError,
    _parse_conc_required,
    _parse_vol_optional,
    _parse_vol_required,
    _ratio,
    nM,
    uL,
    ureg,
)

from .util import maybe_cache_once, gen_random_hash

T = TypeVar("T")


class AbstractAction(metaclass=ABCMeta):
    """
    Abstract class defining an action in a mix recipe.
    """

    @property
    @abstractmethod
    def name(self) -> str:  # pragma: no cover
        ...

    def _get_name(self, _cache_key=None) -> str:
        return self.name

    def tx_volume(
        self,
        mix_vol: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> DecimalQuantity:  # pragma: no cover
        """The total volume transferred by the action to the sample.  May depend on the total mix volume.

        Parameters
        ----------

        mix_vol
            The mix volume.  Does not accept strings.
        """
        return sum(self.each_volumes(mix_vol, actions, _cache_key=_cache_key), Q_("0", "uL"))

    @abstractmethod
    def _mixlines(
        self,
        tablefmt: str | TableFormat,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> Sequence[MixLine]:  # pragma: no cover
        ...

    @abstractmethod
    def all_components(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = (), _cache_key=None
    ) -> pd.DataFrame:  # pragma: no cover
        """A dataframe containing all base components added by the action.

        Parameters
        ----------

        mix_vol
            The mix volume.  Does not accept strings.
        """
        ...

    @abstractmethod
    def with_experiment(
        self: T, experiment: Experiment, *, inplace: bool = True
    ) -> T:  # pragma: no cover
        """Returns a copy of the action updated from a experiment dataframe."""
        ...

    @abstractmethod
    def with_reference(
        self: T, reference: Reference, *, inplace: bool = False
    ) -> T:  # pragma: no cover
        """Returns a copy of the action updated from a reference dataframe."""
        ...

    def dest_concentration(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = (), cache_key=None
    ) -> DecimalQuantity:
        """The destination concentration added to the mix by the action.

        Raises
        ------

        ValueError
            There is no good definition for a single destination concentration
            (the action may add multiple components).
        """
        raise ValueError("Single destination concentration not defined.")

    def dest_concentrations(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = (), cache_key=None
    ) -> Sequence[DecimalQuantity]:
        raise ValueError

    @property
    @abstractmethod
    def components(self) -> list[AbstractComponent]:
        pass

    @property
    def source_concentrations(self) -> list[DecimalQuantity]:
        return self._get_source_concentrations()

    @abstractmethod
    def _get_source_concentrations(self, _cache_key=None) -> list[DecimalQuantity]:
        ...

    @abstractmethod
    def each_volumes(
        self,
        mix_volume: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]: ...

    @classmethod
    @abstractmethod
    def _structure(
        cls, d: dict[str, Any], experiment: Experiment
    ) -> AbstractAction:  # pragma: no cover
        ...

    @abstractmethod
    def _unstructure(
        self, experiment: Experiment | None
    ) -> dict[str, Any]:  # pragma: no cover
        ...


T_AWC = TypeVar("T_AWC", bound="ActionWithComponents")


@attrs.define(eq=False)
class ActionWithComponents(AbstractAction):
    __hash__ = object.__hash__
    components: list[AbstractComponent | str] = attrs.field(
        converter=_maybesequence_comps, on_setattr=attrs.setters.convert
    )

    @property
    def number(self) -> int:
        return self._get_number()

    @maybe_cache_once
    def _get_number(self, _cache_key=None) -> int:
        return len(self.components)

    @property
    def name(self) -> str:
        return ", ".join(c.name for c in self.components)

    def __eq__(self, other: object) -> bool:
        if type(self) != type(other):
            return False
        for a in self.__attrs_attrs__:  # type: ignore
            v1 = getattr(self, a.name)
            v2 = getattr(other, a.name)
            if isinstance(v1, ureg.Quantity):
                if isnan(v1.m) and isnan(v2.m) and (v1.units == v2.units):
                    continue
            if v1 != v2:
                return False
        return True

    def with_experiment(
        self: T_AWC, experiment: Experiment, *, inplace: bool = True
    ) -> T_AWC:
        if inplace:
            self.components = [
                c.with_experiment(experiment, inplace=inplace) for c in self.components
            ]
            return self
        else:
            return attrs.evolve(
                self,
                components=[
                    c.with_experiment(experiment, inplace=inplace)
                    for c in self.components
                ],
            )

    def with_reference(
        self: T_AWC, reference: Reference, *, inplace: bool = False
    ) -> T_AWC:
        if inplace:
            self.components = [  # type: ignore
                c.with_reference(reference, inplace=True) for c in self.components
            ]
            return self
        else:
            return attrs.evolve(
                self, components=[c.with_reference(reference) for c in self.components]
            )

    @property
    def source_concentrations(self) -> list[DecimalQuantity]:
        return self._get_source_concentrations()

    @maybe_cache_once
    def _get_source_concentrations(self, _cache_key=None) -> list[DecimalQuantity]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        concs = [c._get_concentration(_cache_key=_cache_key) for c in self.components]
        return concs

    def _unstructure(self, experiment: Experiment | None) -> dict[str, Any]:
        d: dict[str, Any] = {}
        d["class"] = self.__class__.__name__
        d["components"] = [c._unstructure(experiment) for c in self.components]
        for a in self.__attrs_attrs__:  # type: ignore
            if a.name == "components":
                continue
            val = getattr(self, a.name)
            if val is a.default:
                continue
            # FIXME: nan quantities are always default, and pint handles them poorly
            if isinstance(val, ureg.Quantity) and isnan(val.m):
                continue
            d[a.name] = _unstructure(val)
        return d

    @classmethod
    def _structure(
        cls, d: dict[str, Any], experiment: Experiment | None = None
    ) -> ActionWithComponents:
        scomps: list[AbstractComponent] = []
        for cd in d["components"]:
            if experiment and (cd["name"] in experiment.components):
                scomps.append(experiment.components[cd["name"]])
            elif experiment:
                c = _structure(cd, experiment)
                experiment[c.name] = c
                scomps.append(c)
            else:
                scomps.append(_structure(cd))
        d["components"] = scomps
        for k in d:
            if k == "components":
                continue
            d[k] = _structure(d[k])
        return cls(**d)

    def all_components_polars(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = (), _cache_key=None
    ) -> pd.DataFrame:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key

        all_comps = []

        for comp, dc, sc in zip(
            self.components,
            self.dest_concentrations(mix_vol, actions, _cache_key=_cache_key),
            self._get_source_concentrations(_cache_key=_cache_key),
        ):
            comps: pl.DataFrame = comp.all_components_polars(_cache_key=_cache_key)

            r = _ratio(dc, sc)
            if math.isnan(r):
                r = None
            comps = comps.with_columns(pl.col("concentration_nM").mul(r))

            all_comps.append(comps)

        newdf: pl.DataFrame = pl.concat(all_comps)

        newdf = newdf.group_by("name").agg(
            pl.when(pl.col("concentration_nM").is_null().any())
            .then(pl.lit(None))
            .otherwise(pl.col("concentration_nM").sum())
            .alias("concentration_nM"),
            pl.col("component").first(),  # FIXME
        )

        return newdf

    def all_components(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = ()
    ) -> pd.DataFrame:
        df = self.all_components_polars(mix_vol, actions).to_pandas()
        df.set_index("name", inplace=True)
        return df

    def _compactstrs(
        self,
        tablefmt: str | TableFormat,
        dconcs: Sequence[DecimalQuantity],
        eavols: Sequence[DecimalQuantity],
    ) -> Sequence[MixLine]:
        # locs = [(c.name,) + c.location for c in self.components]
        # names = [c.name for c in self.components]

        # if any(x is None for x in locs):
        #     raise ValueError(
        #         [name for name, loc in zip(names, locs) if loc is None]
        #     )

        locdf = pd.DataFrame(
            {
                "names": [c.printed_name(tablefmt=tablefmt) for c in self.components],
                "source_concs": self.source_concentrations,
                "dest_concs": dconcs,
                "ea_vols": eavols,
                "plate": [c.plate for c in self.components],
                "well": [c.well for c in self.components],
            }
        )

        locdf.fillna({"plate": ""}, inplace=True)

        locdf.sort_values(
            by=["plate", "ea_vols", "well"], ascending=[True, False, True]
        )

        names: list[list[str]] = []
        source_concs: list[DecimalQuantity] = []
        dest_concs: list[DecimalQuantity] = []
        numbers: list[int] = []
        ea_vols: list[DecimalQuantity] = []
        tot_vols: list[DecimalQuantity] = []
        plates: list[str] = []
        wells_list: list[list[WellPos]] = []

        for plate, plate_comps in locdf.groupby("plate"):
            for vol, plate_vol_comps in plate_comps.groupby("ea_vols"):
                if pd.isna(plate_vol_comps["well"].iloc[0]):
                    if not pd.isna(plate_vol_comps["well"]).all():
                        raise ValueError
                    names.append(list(plate_vol_comps["names"]))
                    ea_vols.append(vol)  # type: ignore
                    tot_vols.append(vol * len(plate_vol_comps))  # type: ignore
                    numbers.append(len(plate_vol_comps))
                    source_concs.append(plate_vol_comps["source_concs"].iloc[0])
                    dest_concs.append(plate_vol_comps["dest_concs"].iloc[0])
                    plates.append(plate)  # type: ignore
                    wells_list.append([])
                    continue

                byrow = mixgaps(
                    sorted(list(plate_vol_comps["well"]), key=WellPos.key_byrow),
                    by="row",
                )
                bycol = mixgaps(
                    sorted(list(plate_vol_comps["well"]), key=WellPos.key_bycol),
                    by="col",
                )

                sortkey = WellPos.key_bycol if bycol <= byrow else WellPos.key_byrow

                plate_vol_comps["sortkey"] = [
                    sortkey(c) for c in plate_vol_comps["well"]
                ]

                plate_vol_comps.sort_values(by="sortkey", inplace=True)

                names.append(list(plate_vol_comps["names"]))
                ea_vols.append(vol)
                numbers.append(len(plate_vol_comps))
                tot_vols.append(vol * len(plate_vol_comps))
                source_concs.append(plate_vol_comps["source_concs"].iloc[0])
                dest_concs.append(plate_vol_comps["dest_concs"].iloc[0])
                plates.append(plate)
                wells_list.append(list(plate_vol_comps["well"]))

        return [
            MixLine(
                name,
                source_conc=source_conc,
                dest_conc=dest_conc,
                number=number,
                each_tx_vol=each_tx_vol,
                total_tx_vol=total_tx_vol,
                plate=p,
                wells=wells,
            )
            for name, source_conc, dest_conc, number, each_tx_vol, total_tx_vol, p, wells in zip(
                names,
                source_concs,
                dest_concs,
                numbers,
                ea_vols,
                tot_vols,
                plates,
                wells_list,
            )
        ]


@attrs.define(eq=False)
class FixedVolume(ActionWithComponents):
    """An action adding one or multiple components, with a set transfer volume.

    Parameters
    ----------

    components
        A list of :ref:`Components`.

    fixed_volume
        A fixed volume for the action.  Input can be a string (eg, "5 µL") or a pint Quantity.  The interpretation
        of this depends on equal_conc.

    set_name
        The name of the mix.  If not set, name is based on components.

    compact_display
        If True (default), the action tries to display compactly in mix recipes.  If False, it displays
        each component as a separate line.

    Examples
    --------

    >>> from alhambra.mixes import *
    >>> components = [
    ...     Component("c1", "200 nM"),
    ...     Component("c2", "200 nM"),
    ...     Component("c3", "200 nM"),
    ... ]

    >>> print(Mix([FixedVolume(components, "5 uL")], name="example"))
    Table: Mix: example, Conc: 66.67 nM, Total Vol: 15.00 µl
    <BLANKLINE>
    | Comp       | Src []    | Dest []   |   # | Ea Tx Vol   | Tot Tx Vol   | Loc   | Note   |
    |:-----------|:----------|:----------|----:|:------------|:-------------|:------|:-------|
    | c1, c2, c3 | 200.00 nM | 66.67 nM  |   3 | 5.00 µl     | 15.00 µl     |       |        |
    """

    fixed_volume: DecimalQuantity = attrs.field(
        converter=_parse_vol_required, on_setattr=attrs.setters.convert
    )
    set_name: str | None = None
    compact_display: bool = True

    # components: Sequence[AbstractComponent | str] | AbstractComponent | str, fixed_volume: str | Quantity, set_name: str | None = None, compact_display: bool = True, equal_conc: bool | str = False
    def __new__(cls, *args, **kwargs):
        if (cls is FixedVolume) and ("equal_conc" in kwargs):
            if kwargs["equal_conc"] is not False:
                c = super().__new__(EqualConcentration)
                return c
            else:
                raise ValueError(
                    "FixedVolume no longer supports equal_conc=False, but behaves that way by default.  Remove equal_conc=False and try again."
                )
        c = super().__new__(cls)
        return c

    @maybe_cache_once
    def dest_concentrations(
        self,
        mix_vol: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        return [
            x * y
            for x, y in zip(
                self.source_concentrations,
                _ratio(self.each_volumes(mix_vol, actions, _cache_key=_cache_key), mix_vol),
            )
        ]

    @maybe_cache_once
    def each_volumes(
        self,
        mix_volume: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        return [cast(DecimalQuantity, self.fixed_volume.to(uL))] * len(self.components)

    @property
    def name(self) -> str:
        return self._get_name()
    
    @maybe_cache_once
    def _get_name(self, _cache_key=None) -> str:
        if self.set_name is None:
            return super().name
        else:
            return self.set_name

    @maybe_cache_once
    def _mixlines(
        self,
        tablefmt: str | TableFormat,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[MixLine]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        dconcs = self.dest_concentrations(mix_vol, actions, _cache_key=_cache_key)
        eavols = self.each_volumes(mix_vol, actions, _cache_key=_cache_key)
        if not self.compact_display:
            ml = [
                MixLine(
                    [comp.printed_name(tablefmt=tablefmt)],
                    comp.concentration,
                    dc,
                    ev,
                    plate=comp.plate if comp.plate is not None else "",
                    wells=comp._well_list,
                )
                for dc, ev, comp in zip(
                    dconcs,
                    eavols,
                    self.components,
                )
            ]
        else:
            ml = list(
                self._compactstrs(tablefmt=tablefmt, dconcs=dconcs, eavols=eavols)
            )

        return ml


@attrs.define(init=False, eq=False)
class EqualConcentration(FixedVolume):
    """An action adding an equal concentration of each component, without setting that concentration.

    Depending on the setting of
    `equal_conc`, it may require that the concentrations all be equal to begin with, or may treat the fixed
    transfer volume as the volume as the minimum or maximum volume to transfer, adjusting volumes of each
    strand to make this work and have them at equal destination concentrations.

    Parameters
    ----------

    components
        A list of :ref:`Components`.

    fixed_volume
        A fixed volume for the action.  Input can be a string (eg, "5 µL") or a pint Quantity.  The interpretation
        of this depends on equal_conc.

    set_name
        The name of the mix.  If not set, name is based on components.

    compact_display
        If True (default), the action tries to display compactly in mix recipes.  If False, it displays
        each component as a separate line.

    method
        If `"check"`, the action still transfers the same volume of each component, but will
        raise a `ValueError` if this will not result in every component having the same concentration added
        (ie, if they have different source concentrations).  If `"min_volume"`, the action will transfer *at least*
        `fixed_volume` of each component, but will transfer more for components with lower source concentration,
        so that the destination concentrations are all equal (but not fixed to a specific value).  If `"max_volume"`,
        the action instead transfers *at most* `fixed_volume` of each component, tranferring less for higher
        source concentration components.  If ('max_fill', buffer_name), the fixed volume is the maximum, while for
        every component that is added at a lower volume, a corresponding volume of buffer is added to bring the total
        volume of the two up to the fixed volume.

    >>> components = [
    ...     Component("c1", "200 nM"),
    ...     Component("c2", "200 nM"),
    ...     Component("c3", "200 nM"),
    ...     Component("c4", "100 nM")
    ... ]

    >>> print(Mix([EqualConcentration(components, "5 uL", method="min_volume")], name="example"))
    Table: Mix: example, Conc: 40.00 nM, Total Vol: 25.00 µl
    <BLANKLINE>
    | Comp       | Src []    | Dest []   | #   | Ea Tx Vol   | Tot Tx Vol   | Loc   | Note   |
    |:-----------|:----------|:----------|:----|:------------|:-------------|:------|:-------|
    | c1, c2, c3 | 200.00 nM | 40.00 nM  | 3   | 5.00 µl     | 15.00 µl     |       |        |
    | c4         | 100.00 nM | 40.00 nM  | 1   | 10.00 µl    | 10.00 µl     |       |        |

    >>> print(Mix([EqualConcentration(components, "5 uL", method="max_volume")], name="example"))
    Table: Mix: example, Conc: 40.00 nM, Total Vol: 12.50 µl
    <BLANKLINE>
    | Comp       | Src []    | Dest []   | #   | Ea Tx Vol   | Tot Tx Vol   | Loc   | Note   |
    |:-----------|:----------|:----------|:----|:------------|:-------------|:------|:-------|
    | c1, c2, c3 | 200.00 nM | 40.00 nM  | 3   | 2.50 µl     | 7.50 µl      |       |        |
    | c4         | 100.00 nM | 40.00 nM  | 1   | 5.00 µl     | 5.00 µl      |       |        |
    """
    __hash__ = object.__hash__

    def __init__(
        self,
        components: Sequence[AbstractComponent | str] | AbstractComponent | str,
        fixed_volume: str | DecimalQuantity,
        set_name: str | None = None,
        compact_display: bool = True,
        method: Literal["max_volume", "min_volume", "check"]
        | tuple[Literal["max_fill"], str] = "min_volume",
        equal_conc: bool | str | None = None,
    ):
        if equal_conc is not None:
            warn(
                "The equal_conc parameter for FixedVolume is no longer supported.  Use EqualConcentration and method instead.",
                DeprecationWarning,
                stacklevel=2,
            )

            if equal_conc is True:
                equal_conc = "check"

            method = equal_conc  # type: ignore

        self.__attrs_init__(components, fixed_volume, set_name, compact_display, method)  # type: ignore

    method: (
        Literal["max_volume", "min_volume", "check"] | tuple[Literal["max_fill"], str]
    ) = "min_volume"

    @property
    def source_concentrations(self) -> list[DecimalQuantity]:
        return self._get_source_concentrations()
    
    @maybe_cache_once
    def _get_source_concentrations(self, _cache_key=None) -> list[DecimalQuantity]:
        concs = FixedVolume._get_source_concentrations(self, _cache_key=_cache_key)
        if any(x != concs[0] for x in concs) and (self.method == "check"):
            raise ValueError("Not all components have equal concentration.")
        return concs

    @maybe_cache_once
    def each_volumes(
        self,
        mix_volume: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        # match self.equal_conc:
        if self.method == "min_volume":
            sc = self._get_source_concentrations(_cache_key=_cache_key)
            scmax = max(sc)
            return [self.fixed_volume * x for x in _ratio(scmax, sc)]
        elif (self.method == "max_volume") | (
            isinstance(self.method, Sequence) and self.method[0] == "max_fill"
        ):
            sc = self._get_source_concentrations(_cache_key=_cache_key)
            scmin = min(sc)
            return [self.fixed_volume * x for x in _ratio(scmin, sc)]
        elif self.method == "check":
            sc = self._get_source_concentrations(_cache_key=_cache_key)
            if any(x != sc[0] for x in sc):
                raise ValueError("Concentrations")
            return [cast(DecimalQuantity, self.fixed_volume.to(uL))] * len(
                self.components
            )
        raise ValueError(f"equal_conc={self.method!r} not understood")

    @maybe_cache_once
    def tx_volume(
        self,
        mix_vol: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> DecimalQuantity:
        if isinstance(self.method, Sequence) and (self.method[0] == "max_fill"):
            return self.fixed_volume * len(self.components)
        return sum(self.each_volumes(mix_vol, actions, _cache_key=_cache_key), ureg("0.0 uL"))

    @maybe_cache_once
    def _mixlines(
        self,
        tablefmt: str | TableFormat,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[MixLine]:
        ml = FixedVolume._mixlines(self, tablefmt, mix_vol, _cache_key=_cache_key)
        if isinstance(self.method, Sequence) and (self.method[0] == "max_fill"):
            fv = self.fixed_volume * len(self.components) - sum(
                self.each_volumes(mix_vol, actions=actions, _cache_key=_cache_key)
            )
            if fv != ZERO_VOL:
                ml.append(MixLine([self.method[1]], None, None, fv))
        return ml


@attrs.define(eq=False)
class FixedConcentration(ActionWithComponents):
    """An action adding one or multiple components, with a set destination concentration per component (adjusting volumes).

    FixedConcentration adds a selection of components, with a specified destination concentration.

    Parameters
    ----------

    components
        A list of :ref:`Components`.

    fixed_concentration
        A fixed concentration for the action.  Input can be a string (eg, "50 nM") or a pint Quantity.

    set_name
        The name of the mix.  If not set, name is based on components.

    compact_display
        If True (default), the action tries to display compactly in mix recipes.  If False, it displays
        each component as a separate line.

    min_volume
        Specifies a minimum volume that must be transferred per component.  Currently, this is for
        validation only: it will cause a VolumeError to be raised if a volume is too low.

    Raises
    ------

    VolumeError
        One of the volumes to transfer is less than the specified min_volume.

    Examples
    --------

    >>> from alhambra.mixes import *
    >>> components = [
    ...     Component("c1", "200 nM"),
    ...     Component("c2", "200 nM"),
    ...     Component("c3", "200 nM"),
    ...     Component("c4", "100 nM")
    ... ]

    >>> print(Mix([FixedConcentration(components, "20 nM")], name="example", fixed_total_volume="25 uL"))
    Table: Mix: example, Conc: 40.00 nM, Total Vol: 25.00 µl
    <BLANKLINE>
    | Comp       | Src []    | Dest []   | #   | Ea Tx Vol   | Tot Tx Vol   | Loc   | Note   |
    |:-----------|:----------|:----------|:----|:------------|:-------------|:------|:-------|
    | c1, c2, c3 | 200.00 nM | 20.00 nM  | 3   | 2.50 µl     | 7.50 µl      |       |        |
    | c4         | 100.00 nM | 20.00 nM  |     | 5.00 µl     | 5.00 µl      |       |        |
    | Buffer     |           |           |     |             | 12.50 µl     |       |        |
    | *Total:*   |           | 40.00 nM  |     |             | 25.00 µl     |       |        |
    """

    fixed_concentration: DecimalQuantity = attrs.field(
        converter=_parse_conc_required, on_setattr=attrs.setters.convert
    )
    set_name: str | None = None
    compact_display: bool = True
    min_volume: DecimalQuantity = attrs.field(
        converter=_parse_vol_optional_none_zero,
        default=ZERO_VOL,
        on_setattr=attrs.setters.convert,
    )

    def dest_concentrations(
        self,
        mix_vol: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        return [self.fixed_concentration] * len(self.components)

    @maybe_cache_once
    def each_volumes(
        self,
        mix_volume: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        ea_vols = [
            mix_volume * r
            for r in _ratio(self.fixed_concentration, self._get_source_concentrations(_cache_key=_cache_key))
        ]
        if not math.isnan(self.min_volume.m):
            below_min = []
            for comp, vol in zip(self.components, ea_vols):
                if vol < self.min_volume:
                    below_min.append((comp.name, vol))
            if below_min:
                raise VolumeError(
                    "Volume of some components is below minimum: "
                    + ", ".join(f"{n} at {v}" for n, v in below_min)
                    + ".",
                    below_min,
                )
        return ea_vols

    @maybe_cache_once
    def _mixlines(
        self,
        tablefmt: str | TableFormat,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[MixLine]:
        dconcs = self.dest_concentrations(mix_vol, actions, _cache_key=_cache_key)
        eavols = self.each_volumes(mix_vol, actions, _cache_key=_cache_key)
        if not self.compact_display:
            ml = [
                MixLine(
                    [comp.printed_name(tablefmt=tablefmt)],
                    comp.concentration,
                    dc,
                    ev,
                    plate=comp.plate if comp.plate is not None else "",
                    wells=comp._well_list,
                )
                for dc, ev, comp in zip(
                    dconcs,
                    eavols,
                    self.components,
                )
            ]
        else:
            ml = list(
                self._compactstrs(tablefmt=tablefmt, dconcs=dconcs, eavols=eavols)
            )

        return ml

    @property
    def name(self) -> str:
        if self.set_name is None:
            return super().name
        else:
            return self.set_name


@attrs.define(eq=False)
class ToConcentration(ActionWithComponents):
    """Add an amount of (non-mix) components to result in a fixed total concentration of each in the mix.

    An action adding an amount of components such that the concentration of each component in the mix will
    be at some target concentration.  Unlike FixedConcentration, which *adds* a certain concentration, this
    takes into account other contents of the mix, and only adds enough to reach a particular final
    concentration."""

    fixed_concentration: DecimalQuantity = attrs.field(
        converter=_parse_conc_required, on_setattr=attrs.setters.convert
    )
    compact_display: bool = True
    min_volume: DecimalQuantity = attrs.field(
        converter=_parse_vol_optional,
        default=NAN_VOL,
        on_setattr=attrs.setters.convert,
    )

    @maybe_cache_once
    def _othercomps(
        self, mix_vol: DecimalQuantity, actions: Sequence[AbstractAction] = (), _cache_key=None
    ):
        cps = _empty_components()

        mixcomps = [comp.name for comp in self.components if comp.is_mix]

        if mixcomps:
            raise ValueError(
                f"Some components in ToConcentration are mixes, which is not allowed: {mixcomps}."
            )

        for action in actions:
            if action is self:
                # This action.
                continue
            elif not any(
                x in self.components for x in action.all_components(mix_vol).component
            ):
                # Action has no shared components, so doesn't matter.
                continue
            elif isinstance(action, ToConcentration):
                # Action is another ToConcentration, so makes a mess
                raise ValueError(
                    f"There are two ToConcentration actions with shared components, which is not allowed: {self} and {action}.",
                    self,
                    action,
                )
            mcomp = action.all_components(mix_vol)
            cps, _ = cps.align(mcomp)
            cps.loc[:, "concentration_nM"] = cps.loc[:, "concentration_nM"].fillna(Decimal("0.0")) # type:  ignore
            cps.loc[mcomp.index, "concentration_nM"] += mcomp.concentration_nM
            cps.loc[mcomp.index, "component"] = mcomp.component

        return cps

    @maybe_cache_once
    def dest_concentrations(
        self,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> Sequence[DecimalQuantity]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        if actions:
            _othercomps = self._othercomps(mix_vol, actions, _cache_key=_cache_key)
        else:
            _othercomps = None 
        if _othercomps is not None:
            otherconcs = [
                Q_(_othercomps.loc[comp.name, "concentration_nM"], nM)  # type: ignore
                if comp.name in _othercomps.index
                else ZERO_CONC
                for comp in self.components
            ]
        else:
            otherconcs = [ZERO_CONC for _ in self.components]
        return [self.fixed_concentration - other for other in otherconcs]

    @maybe_cache_once
    def each_volumes(
        self,
        mix_volume: DecimalQuantity = NAN_VOL,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[DecimalQuantity]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        ea_vols = [
            mix_volume * r
            for r in _ratio(
                self.dest_concentrations(mix_volume, actions, _cache_key=_cache_key),
                self.source_concentrations,
            )
        ]
        if not math.isnan(self.min_volume.m):
            below_min = []
            for comp, vol in zip(self.components, ea_vols):
                if vol < self.min_volume:
                    below_min.append((comp.name, vol))
            if below_min:
                raise VolumeError(
                    "Volume of some components is below minimum: "
                    + ", ".join(f"{n} at {v}" for n, v in below_min)
                    + ".",
                    below_min,
                )
        return ea_vols

    @maybe_cache_once
    def _mixlines(
        self,
        tablefmt: str | TableFormat,
        mix_vol: DecimalQuantity,
        actions: Sequence[AbstractAction] = (),
        _cache_key=None,
    ) -> list[MixLine]:
        _cache_key = gen_random_hash() if _cache_key is None else _cache_key
        dconcs = self.dest_concentrations(mix_vol,  actions=actions,_cache_key=_cache_key)
        eavols = self.each_volumes(mix_vol, actions=actions, _cache_key=_cache_key)
        if not self.compact_display:
            ml = [
                MixLine(
                    [comp.printed_name(tablefmt=tablefmt)],
                    comp.concentration,
                    dc,
                    ev,
                    plate=comp.plate if comp.plate is not None else "",
                    wells=comp._well_list,
                )
                for dc, ev, comp in zip(dconcs, eavols, self.components)
            ]
        else:
            ml = list(
                self._compactstrs(tablefmt=tablefmt, dconcs=dconcs, eavols=eavols)
            )

        return ml


MultiFixedConcentration = FixedConcentration
MultiFixedVolume = FixedVolume

for c in [FixedConcentration, FixedVolume, EqualConcentration, ToConcentration]:
    _STRUCTURE_CLASSES[c.__name__] = c
