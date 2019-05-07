# Chart of the Nuclides

To create materials in FRIDGe, the corresponding elements must be present in the directory `fridge/data/CotN`.
Each element needs is own YAML file and contains seven variables for inputting data; where each variable and its associate input can be seen in Table \ref{tab:element}

[tab: elements](Variables for Element YAML file.)
| Variable Name                   | Variable Type    | Unit     | Example                           |
|---------------------------------|------------------|----------|-----------------------------------|
| Name                            | string           | --       | Silicon                           |
| ZAID                            | integer          | --       | 14000                             |
| Isotopes                        | list of integers | --       | [14028, 14029, 14030]             |
| Abundance                       | list of floats   | weight % | [0.92223, 0.04685, 0.0392]        |
| Mass                            | list of floats   | amu      | [27.976926, 28.976494, 29.973777] |
| Density                         | float            | g/cc     | 2.33                              |
| Linear Coefficient of Expansion | float            | K^-1     | 2.432e^-6                         |