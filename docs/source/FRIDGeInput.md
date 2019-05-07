# FRIDGe Input

The FRIDGe input file is used to denote general properties for the MCNP input file, and what core/assembly to make, these files can be found int `fridge/fridge_input_files`. 
There are currently 16 options that can be included in the FRIDGe input file, Table 1 gives a descriptions of each one and the default value.

Table 1. Variables for FRIDGe Input YAML file.

|Variable Name   | Variable Type | Unit | Example | Default|
|----------------|---------------|------|---------|--------|
|Name  | string | -- | FRIDGe\_Test | |
|Input Type  | string | -- | Core | Single|
|Output File Name<sup>*</sup>  | string | -- | File23 | FRIDGe1|
|Temperature<sup>*</sup> | int | K | 1200 | 900|
|XC Library<sup>*</sup> | string | -- | ENDFVII.0 | ENDFVII.1|
|Number of Generations<sup>*</sup> | int | -- | 1000 | 230|
|Number of Skipped Generations<sup>*</sup> | int | -- | 50 | 30|
|Number of Particle Per Generations<sup>*</sup> | int | -- | 1e8 | 1e6|
|Run Kinetics<sup>*</sup> | Boolean | -- | True | False|
|Void Percent<sup>*</sup> | float | \% | 0.1 | 1.0|
|ksens<sup>*,**</sup> | Boolean | -- | True | False|
|Temperature Adjusted Density<sup>*,**</sup> | Boolean | -- | True | False|
|Temperature Adjusted Volume<sup>*,**</sup> | Boolean| -- | True | False|
|Smear Clad<sup>*,**</sup> | Boolean | -- | True | False|
|Smear Bond<sup>*,**</sup> | Boolean | -- | True | False|

<sup>*</sup>Optional

<sup>**</sup>Currently not built into FRIDGe.

The only variables required for building a FRIDGe input file are the `Name` and `Input Type`, all other variables have default setting.
The `Name` is assembly or core file which will be used.
The `Input Type` is the the type of file to be create, two options are available; Single and Core.
`Output File Name` will denote the name of the MCNP input file, `.i` file, that will be created.
`Temperature` is the temperature of the system denoted in Kelvin, currently there are three options; 600, 900, and 1200.
`XC Library` is the name of the cross section library that will be used, currently there are three options; ENDFVII.0, ENDFVII.1, JEFF3.1.
Note: The combination of `Temperature` and `XC Library` will select the appropriate cross-section set for each material used.
`Number of Generations` is the MCNP number of generations that the simulation will run for.
`Number of skikpped Generations` is the MCNP number of generations that are skipped before statistics are started.
`Number Particles per Generation` is the number of particles that will be run for each generation.
`Run Kinetics` will implement the `kopts` portion of code for MCNP, the default setting for `kopts` are currently used.
The remaining settings are currently not used in FRIDGe, but are intended for addition.
A description of each will be added as each variable is added.
