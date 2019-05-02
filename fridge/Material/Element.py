import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
element_dir = os.path.join(cur_dir, '../data/CotN/')


class Element(object):
    """Creates an element based on the Chart of the Nuclide Database."""
    def __init__(self, element):
        element_yaml_file = glob.glob(os.path.join(element_dir, element + '.yaml'))

        if not element_yaml_file:
            self.error = "Element {}, not found in Chart of the Nuclide Database. " \
                                 "Please create element file for {}.".format(element, element)
            raise AssertionError(self.error)

        with open(element_yaml_file[0], "r") as file:
            inputs = yaml.safe_load(file)
            self.name = inputs['Name']
            self.zaid = inputs['ZAID']
            self.isotopes = inputs['Isotopes']
            self.molecularMass = inputs['Mass']
            self.density = inputs['Density']
            self.abundance = inputs['Abundance']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']
            self.atomPercentDict = {}
            self.molecularMassDict = {}
            self.elementalMolecularMass = 0
            self.weightPercentDict = {}
            for num, isotope in enumerate(self.isotopes):
                self.atomPercentDict[isotope] = self.abundance[num]
            for num, isotope in enumerate(self.isotopes):
                self.molecularMassDict[isotope] = self.molecularMass[num]

            for k, v in self.atomPercentDict.items():
                self.elementalMolecularMass += self.molecularMassDict[k] * v

            if not all(v == 0 for v in self.abundance):
                for k, v in self.atomPercentDict.items():
                    self.weightPercentDict[k] = self.molecularMassDict[k] * v / self.elementalMolecularMass
