#FRIDGe Input

The FRIDGe input file is used to denote general properties for the MCNP input file, and what core/assembly to make, these files can be found int `fridge/fridge_input_files`. 
There are currently 16 options that can be included in the FRIDGe input file, Table 1 gives a descriptions of each one and the default value.

Table 1. Variables for FRIDGe Input YAML file.

|Variable Name   | Variable Type | Unit | Example | Default| 
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