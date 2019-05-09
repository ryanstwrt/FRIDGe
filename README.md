[![Build Status](https://travis-ci.org/ryanstwrt/FRIDGe.svg?branch=master)](https://travis-ci.org/ryanstwrt/FRIDGe)
[![Coverage Status](https://coveralls.io/repos/github/ryanstwrt/FRIDGe/badge.svg?branch=master)](https://coveralls.io/github/ryanstwrt/FRIDGe?branch=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# FRIDGe
Fast Reactor Input Deck Generator is a general purpose fast reactor MCNP input deck creator.
Currently FRIDGe has the ability to create two different types of assemblies; fuel and smear.
These assemblies can the be arranged to create a full reactor core model.
The input file gives the user the ability to set the temperature, cross-section set, and MCNP variables for a given problem.

# Documentation

Documentation can be found [Here](https://ryanstwrt.github.io/FRIDGe/).
This documentation holds all of the information to build elements, materials, assemblies, cores, and FRIDGe input files.
FRIDGe comes packaged with 24 elements, 8 materials, 2 assemblies, and 1 FRIDGe input file pre-built.
Along with this there are 3 test assemblies, 1 test core, and 4 test FRIDGe input files that can be used as a template for building these files.

# Install

To download FRIDGe, change into your directory of choice and follow the instructions below:

```bash
git clone https://github.com/ryanstwrt/FRIDGe
```

# Testing

It is encouraged to run the test suite built into FRIDGe before creating any models. Testing FRIDGe is relatively simple.
Open a terminal in the ```/fridge``` directory and run the following:

```bash
python -m pytest
```

Note: pytest, PyYAML, and numpy are ball required to run FRIDGe, and the test suite.

# Running FRIDGe

FRIDGe has a prebuilt input file which can be used to gain familiarity with running FRIDGe.
The FRIDGe input file that will be used is title ```EBRII_Driver.yaml```, and is uses the assembly file ```EBRII_MKII.yaml```.
These two YAML files can be found in ```/fridge/fridge_input_files``` and ```/fridge/data/assembly```, respectively.

The first step is to open an interactive python terminal in the ```fridge``` directory.
From here, import the FRIDGe driver with the following:
```bash
import fridge.driver.fridge_driver as fd
```
The driver for FRIDGe has now been imported, and the main function can be run via:
```bash
fd.main(''<fridge_input_file>'')
```
For this example the following code can be run:
```bash
fd.main('EBRII_Driver')
```
This will cause FRIDGe to build an MCNP input file in ```/fridge/mcnp_input_files``` titled ```EBRII_Driver.i```.
This example built a single assembly; the process for running FRIDGe and building a full core model is identical.

# Development

As FRIDGe is open source, I encourage anyone who is interested to contribute and add to the code.
There are multiple phenomena that could be incorporated into FRIDGe to produce a more realistic model.

# Contact

Please feel free to email me at stewryan@oregonstate.edu if you have any questions or if you would like me to consider additional features.
