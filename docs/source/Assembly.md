<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

# Assemblies

There are two types of assemblies that can be built in FRIDGe; smear and fuel assemblies.
Both types of assemblies are created using YAML files and can be found in `fridge/data/assembly`.

## Smear Assemblies

Smear assemblies are

Table 1. Variables for Smear Assembly YAML file.

|Variable Name   | Variable Type | Unit | Example|
|----------------|---------------|------|--------|
|Assembly Type  | string | -- | Blank|
|Assembly Pitch | float  | cm | 12.0|
|Duct Thickness | float | cm | 0.3|
|Duct Inside Flat to Flat | float | cm | 11.1|
|Assembly Height | float | cm | 240|
|Coolant | string | -- LiquidNa|
|Assembly Material | string | -- | HT9|
|Blank Height | float | cm | 220|
|Blank Smear | Dictionary | {str: wt \%} | {LiquidNa: 0.9, HT9: 0.1}|
|Z Position | float | cm | -60|

`Assembly Type` is a string used to denote the types of assembly (smear or fuel).
`Assembly Pitch` is a float to denote the distance from the center of one assembly to an adjacent assembly.
Note: All assemblies in a core should have the same assembly pitch; if they don't errors in geometry may arise.
`Duct Thickness` is a float do denote the thickness of the assembly duct.
`Duct Inside Flat to Flat` is a float to denote the distance from one side of a hexagon to the other.
`Assembly Height` is a float used to denote the total height of the assembly.
`Coolant` is a string used to create a material for the coolant.
`Assembly Material` is a string used to create a material for the assembly.
`Blank Height` is a float used to denote the height of the smear portion of the assembly.
Note: If `Blank Height` of the assembly exceeds the `Assembly Height`, the `Assembly Height` will truncate the `Blank Height`, this may lead to geometry errors.
`Blank Smnear` is a dictionary of strings and weight percents.
This will create a smeared material where each string in the dictionary will create a material, whose weight fraction is the corresponding float.
`Z Position` is a float which allows the user to manually adjust where they want the bottom of the smear assembly to be.

## Fuel Assembly

`Assembly Type` is a string used to denote the types of assembly (smear or fuel).
`Assembly Pitch` is a float to denote the distance from the center of one assembly to an adjacent assembly.
Note: All assemblies in a core should have the same assembly pitch; if they don't errors in geometry may arise.
`Duct Thickness` is a float do denote the thickness of the assembly duct.
`Duct Inside Flat to Flat` is a float to denote the distance from one side of a hexagon to the other.
`Assembly Height` is a float used to denote the total height of the assembly.
`Coolant` is a string used to create a material for the coolant.
`Assembly Material` is a string used to create a material for the assembly.
`Pins Per Assembly` is an integer of the number of pins for the assembly.
Note: This number should fit an exact number of rings required, Table 5, shows pins are required for a given number of rings.

`Pin Diameter` is a float which is the diameter of the fuel pin (outside of the cladding).
`Clad Thickness` is a float to denote the cladding thickness.
`Fuel Smear` is a float to denote the percentage of area inside the cladding that the fuel encompasses.
The relation between the fuel diameter and fuel smear can be seen below, where $R_{IC}$ is the inner cladding radius, and $A_fuel$ is the `Fuel Smear`.

`Fuel Diameter` is a float to denote the diameter of the fuel slug.
`Pitch` is a float to denote the distance from the center of one fuel pin to an adjacent fuel pin.
`Wire Wrap Diameter` is a float to denote the diameter of the wire wrap.
Note: The diameter of the pin plus the diameter of the wire wrap should not exceed the pitch.
FRIDGe will allow this, but it is not physically possible.
`Wire Wrap Axial Pitch` is a float which denotes the distance between each wrap.
`Fuel Height` is a float to denote the height of the fuel pin.
`Fuel` is a string to denote the fuel material.
`Clad` is a string to denote the cladding material.
`Bond` is a float to denote the fuel bond material.
`Bond above Fuel` is a float to denote the height of the bond above the fuel.
`Plenum Height` is a float used to denote the height of the plenum portion of the assembly.
`Plenum Smear` is a dictionary of strings and weight percents.
This will create a smeared material where each string in the dictionary will create a material, whose weight fraction is the corresponding float.
`Reflector Height` is a float used to denote the height of the reflector portions of the assembly.
`Reflector Smear` is a dictionary of strings and weight percents.
This will create a smeared material where each string in the dictionary will create a material, whose weight fraction is the corresponding float.


