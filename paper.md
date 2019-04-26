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
Often times, a core design process starts with examining the neutronic viability.
This process is too complex to be done by hand, and requires the use of sophisticated software suites to perform.
Utilizing additional software comes at the cost of learning the nuances of each particular program.
For example, how does one create the geometry or materials in question.
This process is different for each suite utilized, and often distracts from the core design process.
Input files for such program can grow exceeding large (over 10,000 lines) when trying to describe a heterogenous core.
At this size, it is often unrealistic to manually adjust values and expect a functioning model.

FRIDGe was created to help alleviate the process of learning additional code nomenclature when designing and testing fast reactors.
The only inputes the user focuses on are directly related to the core design process.
This allows the user to focus on what aspects of the design affect the reactor, rather than wondering if they created the model.

FRIDGe currently houses the capability to create input files for single assembly or full core analysis in the code suite MCNP.
This process is done by utilizing yaml files that the user has direct control over; assembly, core, and input.
The assembly file is used for individual assemblies, where the user can specify their geometry and materials.
The core file is used to create a full reactor core based on individual assemblies.
The input file has control over general setting for the reactor model such as temperature, cross-section sets, etc.
With these three files types, a user needs to specify what types of assemblies they are making, where they go in the core, and what setting they desire to create a full core assembly.
Along with these files there are two other types of files which control the elemental and material compositions which can also be utilized created should the need arise.



