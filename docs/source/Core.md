# Core

A core is built by placing any number of assemblies into any position within the core.
It is created using a YAML file, which can be found in `fridge/data/core` and requires four variables in addition to $n$ number of assembly positions.
Table 1 shows the requirements for a core file.

Table 1. Variables for Core YAML file.

|Variable Name   | Variable Type | Unit | Example|
|----------------|---------------|------|--------|
|Name  | string | -- | TestCore|
|Vessel Thickness | float | cm | 10.0|
|Vessel Material | string | -- | HT9|
|Coolant Material | string | -- | LiquidNa|
|Assembly Positions | dictionary | str: str | 01A01: TestAssembly|

`Name` is a string used to denote the name of the core.
`Vessel Thickness` is a float do denote the thickness of the vessel both axially and radially. 
`Vessel Material` is a string used to create a material for the reactor vessel. 
`Coolant Material` is a string used to create the coolant for the reactor vessel. 
Note: This will overwrite any coolant material assigned to an assembly. 
`Assembly Position` is used to describe each assembly in the core, and what assembly goes there. 
The first entry is a five character string which broken into a triplet. 
The first two number denote the ring, the letter denotes the hextant, and the last two numbers denote the number of assemblies off the hextant axis. 
Figure 1, shows the nomenclature used to describe each position.

Figure 1. Description of assembly positions.

![Core](FullCore.png)