# Materials

Materials can be found in the directory `fridge/data/materials`.
Each material in a problem requires its own YAML file and can be created using a material mass fraction or atom density.
Table 1 contains vairables that are required and associated with each input type.
Tables 2 - 3 present the variables associated with each selction type.

Table 1. Common Variables for Material YAML file.

|Variable Name   | Variable Type | Unit | Example|
|----------------|---------------|------|--------|
|Name  | string | -- | UO2|
|Elements | list of strs | -- | [U, O]|
|Elemental ZAIDs | list of ints | -- | [92000, 8000]|
|Linear Coefficient of Expansion | float | K<sup>-1</sup> |0.0|

`Name` is a string containing the name of the element.
`Elements` is a list of element symbols to be used in the material.
**Note:** This element symbol is how FRIDGe finds the element in `fridge/data/CotN`, so ensure that the elements exists there and the symbol matches.
`Elemental ZAIDs` is list of integers, where each ZAID is denoted by 1000 * Z.
`Linear Coefficient of Expansion` is the coefficient of thermal expansion in K<sup>-1</sup>.

Table 2. Variables for Matrial YAML file using Mass Fraction.

|Variable Name   | Variable Type | Unit | Example|
|----------------|---------------|------|--------|
|Elemental Weight Fractions | list of floats | wt % | [0.881467, 0.118533]|
|Enrichment Adjustment ZAIDs<sup>*</sup> | list of ints | -- | [92000, 8000]|
|Isotopic Adjustment ZAIDs<sup>*</sup> | list of list of ints | -- | [[92234, 92235, 92238], [8016, 8017, 8018]]|
|Isotopic Weight Percents<sup>*</sup> | list of list of floats | wt % | [[0.0, 0.03, 0.97], [1.0, 0.0, 0.0]]|
|Density | float | g/cc | 2.33|

<sup>*</sup> Optional variables if material has specific isotopics.

`Elemental Weight Fractions` is a list of floats whose entries are the weight fractions associated with the `ZAIDs` above.
**Note:** This value should sum to 1.0.
`Elemental Adjustment ZAIDs` is a list of ZAIDs whose isotopic fraction is different from the base element.
**Note:** If the isotopic composition is the same as the element in question, the element does not need to be included and it will be created as normal.
`Isotopic Adjustment ZAIDs` is a list of lists of isotopic ZAIDs, where each list corresponds to the the  `Elemental Adjustment ZAIDs` from above.
`Isotopic Weight Percents` is a list of lists of weight fractions (enrichment) of each isotope from `Isotopic Adjustment ZAIDs`.
**Note:** Each list should sum 1.0.
**Note:** If the element `Abundance` has a value, other than 0.0, for the weight percent, it must be included in the `Isotopics Adjustment ZAIDs` and the `Isotopic Weight Percents`.
For example, in Table 2, Uranium includes 92234 and sets the `Isotopic Weight Percent` to 0.0.
This will overwrite the elemental `Abundance` value of 0.000054 with 0.0, otherwise the total weight percent for uranium would be 1.000054.
The `Isotopic Adjustment ZAIDs` of 92233 and 92236 for Uranium are not included because their weight percents are 0.0 in the elements `Abundance`.
`Density` is the density of the material in g/cc.

Table 3. Variables for Matrial YAML file using Atom Densities.

|Variable Name   | Variable Type | Unit | Example|
|----------------|---------------|------|--------|
|Isotopic ZAIDs  | list of list of ints| -- | [[92234, 92235, 92236, 92238], [8016, 8017, 8018]] |
|Isotopic Atom Densities | Dictionary | int:float | {92234: 0.000007, 92235: 0.000743, ... } |
|Density<sup>&dagger;</sup> | float | g/cc | 2.33|
|Molecular Mass<sup>&dagger;</sup> | float | g/mol | 2.33|
|Atom Density | float | a/bn-cm | 0.73348 |

<sup>&dagger;</sup> Either density or molecular mass must be specified.

`Isotopic ZAIDs` is a list of a list of isotopic ZAIDs, where each inner list corresponds to a the specific ZAIDs isotopes that are present in the material.
`Isotopic Atom Densities`is a dictionary of isotopic ZAIDS, where the key is the ZAID number and the value is the atom density for that ZAID.
`Density` is the density of the material in g/cc.
`Molecular Mass` is the molecular mass of the material in g/mol.
`Atom Density` is the atom density of the material in atoms/barn-cm.
