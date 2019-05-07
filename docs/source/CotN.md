# Chart of the Nuclides

To create materials in FRIDGe, the corresponding elements must be present in the directory `fridge/data/CotN`.
Each element needs is own YAML file and contains seven variables for inputting data; where each variable and its associate input can be seen in Table [tab: elements].

![tab: elements](FRIDGe/fridge/docs/source/ElementsTable.PNG)

`Name` is a string containing the name of the element.
`ZAID` is an integer denoted by 1000 * Z (proton or atomic number).
`Isotopes` is a list of ZAID's for each isotope in the element denoted by 1000 * Z + N, where N is the mass number (protons + neutrons) of the isotope.
`Abundance` is a list of the natural abundances for the isotopes (this is in weight percent and can be found in any Chart of the Nuclide).
Note: for elements with no natural abundances an entry of zero is allowed. The abundance can be set later in the material card.
`Mass` is a list of nuclide masses for each isotope listed and is given in amu's.
All abundances and masses were obtained using IAEA's Live Chart of Nuclides \cite{CotN}.
`Density` is the density of the natural isotope in g/cc.
`Linear Coefficient of Expansion` is the coefficient of thermal expansion and is in units of $K^{-1}$.
