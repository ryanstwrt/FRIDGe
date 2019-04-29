---
title: 'FRIDGe: Fast Reactor Input Deck Generator'
tags:
  - Python
  - nuclear engineering
  - reactor design
  - fast reactors
authors:
  - name: Ryan H. Stewart
    affiliation: "1"
    orchid: 0000-0003-4867-6555
affilitaions:
  - name: Oregon State University
    index: 1
date: 25 April 2019
---

# Summary

Reactor core design for nuclear engineers is an extremely complex topic which requires skills in multiple areas of study.
Often, a core design process starts with examining the neutronic viability.
This process is too complex to be done by hand and requires the use of sophisticated software suites to perform.
Utilizing additional software alleviates solving the fundamental physics associated with core design but comes at the cost of learning the nuances of software suites.
Much of the software used are multi-purpose and not specialized for core design.
Typically each requires building and input deck that incorporates geometry, materials, and the appropriate physics to utilized.
This requires the designer to shift their focus from core design to input file management, which takes away their ability to critically think about core design.
Learning how to create these input files by hand can be frustrating and prone to error.
This is especially the case when trying to model a full heterogeneous core where the input decks can grow exceedingly large (over 10000 lines).
At this size, it is unrealistic to manually adjust values and expect a functioning model free of errors.

FRIDGe was created to help alleviate the process of learning additional code nomenclature when designing, modeling, and testing fast reactors.
The only inputes the user focuses on are directly related to the core design process and create a level of abstraction from the input deck generated.
This allows the user to focus on what aspects of the design affect the reactor, rather than input file creation and management.

FRIDGe currently houses the capability to create input files for single assembly or full core analysis in the code suite MCNP.
This process is done by creating a series of yaml files for the materials, assembly, core and general input file.
The material file allows the user to create custom materials (fuels, cladding, poisons, etc.) that the model will require.
The assembly file is used for individual assemblies, where the user can specify the assembly type, geometry, and materials used.
The core file is used to determine the assemblies present and their position within the core.
The input file has control over general setting for the reactor model and any additional features to be applied to the model.
With these files, a user needs to specify what types of assemblies they are making, what materials they are made of, and where they go in the core to create a full fast reactor model.
