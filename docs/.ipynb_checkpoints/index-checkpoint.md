# Fast Reactor Input Deck Generator (FRIDGe)

## Overview

The Fast Reactor Input Deck Generator (FRIDGe) is a tool for designing and building input files for MCNP.
It grants the user the ability to create elements, materials, assemblies, and full reactor cores.
Full reactor cores allow for heterogenous assembly placement with the advent of a core map.
Reacto assemblies can be built using two types of assemblies: heterogenous and homogenous assemblies.
Homogenous assemblies are most commenly used as reflectors, shields, or blank assemblies.
Heterogenous cores allow for the creation of a pin lattice, which is explicetly modeled and is typically used for fuel or control assemblies.
Both assembly types allow for variable axial components to allow a diverse set of assemblies to be described.

FRIDGe currently contains 31 elements, and a handful of materials which are most commonly used in the development of fast reactors.
There are also examples of both assembly and core files provided to be used as templates.

## MCNP Data Extraction and Database Creation

FRIDGe has the ability to read MCNP output files and extract various data from it.
Data scraped from the MCNP output file includes basic neutronic parameters, such as the k-eigenvalue, neutron kinetics, and other parameters found in the output file.
If a burnup run is read, the extracter will read the base neutronic paramters from each burnup step along with assembly specific burnup information.
The assembly specific burnup information includes assembly averaged burnup, actinide nuclide inventories, and assembly power fraction.
All data extracted from an MCNP output file is placed in an H5 database, to allow for convenient access.

## Validation

Currently in progress is a model for the Fast Flux Test Facility benchmark in the IRPhEP[1].

In addition to a full benchmark, material validation has been performed using the *Compendium of Material Composition Data for Radiation Transport Modeling* [2].
This ensuring materials are converted to atom percent corectly, and that the atom density is calculated to within 1E-4 of the known atom density.

# Contents
* [Data](source/Data.md)

* [Test Suite](source/Test.md)

* [Running FRIDGe](source/Run.md)

* [Example](source/Examples.md)

## References
[1] “International Handbook of Evaluated Reactor Physics Benchmark Experiments,” NEA/NSC/DOC(2006)1, Organisation for Economic Co-operation and Development/Nuclear Energy Agency (2018).
[2] R. J. McCONN et al., “Compendium of Material Composition Data for Radiation Transport Modeling,” PNNL-15870, Rev. 1, Pacific Northwest National Laboratory (2011).  