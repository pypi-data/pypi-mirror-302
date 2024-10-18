.. currentmodule:: alhambra_mixes

User's guide
============

Concepts
--------

Alhambra-mixes is a small library to make it easier to organize complicated, hierarchical mixes.

Alhambra-mixes organizes the mixing process into several concepts:

- A *Component* is something that goes into a mix, and has a source concentration.  It may be a generic component, a strand with a sequence, or a mix.  It may also contain information about
- An *Action* describes how a component or set of components is to be added to a mix.  It may specify that each component be added to get a target concentration in the mix, for example, or that a fixed volume of each component be added.  For example, the `FixedConcentration` action adds a component (or several components) to a mix at a fixed desired concentration, while `FixedVolume` adds components at fixed volumes.
- A *Mix* is a collection of Actions, each covering some Components.  It may have a fixed volume, or that may be determined by the components.  It may also have a fixed effective concentration (for use as a component), or that may be determined by a particular component.
- A *Reference* is an object that has information about component concentrations, sequences, and locations.
- An *Experiment* collects many mixes/components.  These are not necessary, but allow saving and loading to and from files, tracking of produced and used concentrations, and referencing of other components and mixes by name.

Physical units are used extensively in alhambra-mixes.  Internally, the library uses pint to handle units, and the decimal library to handle numbers, to avoid floating point inaccuracies.  While using the library, units can be specifid flexibly as strings, which will be processed as the correct quantity, for example `"50 nM"`, or `"10 µL"`,
or `"5 uM"`.  If you need to do calculations, quantities can be created using :any:`Q_`, for example, `Q_(10, "µL")`,
or `Q_("55.3", "nM")`, and these values can be used with normal arithmetic operations.

.. code-block:: python

   ref = Reference.compile(["idt-spec-sheet-1.xlsx", ("idt-order-2.xlsx", "100 µM")])

   mg = Component("10x Mg in TE buffer", "125 mM")

   strands = [Strand(f"strand_{i}") for i in range(0, 10)]

   strand_individual = Strand("extra_strand", sequence="AGATTAGCTCC").with_reference(ref)

   mix1 = Mix(
      [
         MultiFixedConcentration(strands, "1 µM"),
         FixedConcentration(strand_individual, "2 µM"),
         FixedConcentration(mg, "125 mM")
      ],
      name = "mix_with_concentrations",
      fixed_total_volume = "100 µL"
   )

   mix2 = Mix(
      [
         MultiFixedVolume(strands, "5 µL", equal_conc="min_volume")
      ],
      name = "mix_with_volumes"
   )

Components
----------

A component is something that is added to a mix.  It must have a `name`, and generally includes some other information, such as concentration, a tube or plate and well location, or a DNA sequence.  A :any:`Mix` is also, itself, a component that can be reused in other mixes.

Components are usually created by using their classes.  For simple systems, they can be be specified directly,
for example,

.. code-block:: python

   strand = Strand("H_N_5", "100 uM", "GGAGTCCATTCG", plate="plate1", well="A3")

For more complex systems, information will often be in a reference file.  In that case, partially specified components can be used, and the details filled in with the reference.  `.with_reference(ref)` will search for a matching component in the reference `ref`, and return a component with details added.  For example:

.. code-block:: python

   strand = Strand("H_N_5").with_reference(ref)

Adding details beyond a name may be useful, in order to ensure that the details in the reference match, or to find a particular item in the reference, for example, specifying that you'd like a component in a particular plate, or at a particular concentration, if you have multiple copies of it.

.. code-block:: python

   strand = Strand("H_N_5", plate="plate2")

In order to be used in a mix, a component should have at least a name and concentration.  However, these can be omitted when adding them to a mix, and added later (for example, `Mix.with_reference` will add reference details recursively to components in a mix), or may be calculated automatically (a `Mix` will often have a "mix concentration" calculated based on its components).

.. autosummary::

   Component
   Strand
   Mix

.. note::
   Components implement the :any:`AbstractComponent` class.

Actions
-------

Actions describe how a component, or set of components, should be added to a mix.  An action can be seen as a collection of related pipetting steps.

There are two main actions.  `FixedConcentration` is useful when you'd like to add a fixed concentration of each component to a mix, but you don't care about the volume being transferred, beyond potentially wanting to ensure that it is above a certain minimum.  `FixedVolume` is useful when you'd like to add a fixed volume of each component.  There is also `EqualConcentration`, when you'd like to transfer some volume of a number of components so the same concentration of each is added, and `ToConcentration`, which adds (non-mix) components so that, taking into account everything else in the mix recursively, those components will each be at a particular concentration.

.. autosummary::

  FixedVolume
  FixedConcentration
  EqualConcentration
  ToConcentration

.. note::
   Previous versions of alhambra_mixes only supported single components for `FixedVolume` and `FixedConcentration`, and included separate `MultiFixedVolume` and `MultiFixedConcentration`  classes for multiple components.  The two `Multi` class names are currently kept for compatibility reasons, as aliases of `FixedVolume` and `FixedConcentration`.  `FixedVolume` originally implemented the features of `EqualConcentration`, but this was confusing: the `equal_conc` parameter to `FixedVolume` is deprecated, but will try to create a corresponding `EqualConcentration` instance.  Note that `FixedVolume` originally by default gave an error if destination concentrations were different; it no longer does so, and simply transfers fixed volumes.

   Actions must implement the :any:`AbstractAction` class.  For convenience, there's the :any:`ActionWithComponents` class, which is generally applicable for actions that act on a list of components.

Mixes
-----

The `Mix` class represents a mix, which is defined as a set of actions, a name, and potentially some other information, like fixed total volume, a minimum desired transfer volume, or a way to define the mix's concentration.

.. autosummary::
   Mix

.. autosummary::
   Mix.with_reference

The easiest way to display mixes is through Jupyter notebooks.  Simply displaying (or using `display`) a mix will output a formatted table.  Additionally, there are several methods:

.. autosummary::
   Mix.display_instructions
   Mix.instructions
   Mix.plate_maps
   Mix.tubes_markdown

Many methods can accept a `tablefmt` parameter, based on the tabulate package, which chooses what format the output should be.  The useful tablefmt values include "pipe" (a pandoc-compatible Markdown table), "github" (a github-and-pandoc-compatible Markdown table), "unsafehtml" (an HTML table), "latex", and "orgtbl".

Mixes can also provide information on the individual components they contain, calculated recursively if there are multiple levels of mixes involved:

.. autosummary::
   Mix.all_components

References
----------

While alhambra-mixes can be used while specifying all component information directly, it is often more useful to collect that information from other sources.

.. autosummary::
   Reference
   Reference.compile
   Reference.update
   Reference.from_csv
   Reference.to_csv

With this reference, components, actions, and mixes can be updated with the information in them:

.. autosummary::
   Mix.with_reference
   AbstractAction.with_reference
   Component.with_reference

Experiments
-----------

Experiments hold mixes, and potentially concentrations, to be referred to later and tracked as a group.

Mixes can be added to an experiment using the :any:`Experiment.add_mix` method, or by using `experiment[mix_name] = Mix(...)`.  In the latter case, the name in the Mix does not need to be set: it will be set to `mix_name` when it is added to the experiment.  When mixes are added, components that are string references are resolved to components with the same names in the experiment.  This is obviously not possible if the mix being referred to is only added later: in this case, you can use the :any:`Experiment.resolve_components` method to resolve the references.

A useful feature of an Experiment is that the consumed and produced volumes of mixes, and the consumed volumes of other components, can be tracked across all of the mixes involved:

.. autosummary::
   Experiment.check_volumes
   Experiment.consumed_and_produced_volumes

Experiments also allow groups of mixes to be saved and loaded to JSON files.  When written, any mixes used in other mixes are replaced with references to those mixes, so that when the file is loaded, the mixes are linked back together, and changes to one mix in the experiment will propagate to all the mixes that use it:

.. autosummary::
   Experiment.save
   Experiment.load
