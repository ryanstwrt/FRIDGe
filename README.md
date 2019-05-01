[![Build Status](https://travis-ci.org/ryanstwrt/svg?branch=master)](https://travis-ci.org/ryanstwrt/FRIDGe)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# FRIDGe
Fast Reactor Input Deck Generator is a general purpose fast reactor MCNP input deck creator.
Currently FRIDGe has the ability to create two different types of assemblies; fuel and blank.
These assemblies can the be arranged to create a full reactor core model.
The input file gives the user the ability to set the temperature, cross-section set, and MCNP variables for a given problem.

# Documentation

Documentation can be found in ```/fridge/docs```.
This documentation holds all of the information to build elements, materials, assemblies, cores, and FRIDGe input files.
FRIDGe comes packaged with 24 elements, 8 materials, 2 assemblies, and 1 FRIDGe input file that are pre-built.
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

# Development

As FRIDGe is open source, I encourage anyone who is interested to contribute and add to the code.

# Contact

Please feel free to email me at stewryan@oregonstate.edu if you have any questions or if you would like me to consider additional features.