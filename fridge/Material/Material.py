import numpy as np
import glob
import os
import yaml
import fridge.Material.Element as Element

AVOGADROS_NUMBER = 0.6022140857
# Requirements for the material reader
cur_dir = os.path.dirname(__file__)
material_dir = os.path.join(cur_dir, '../data/materials/')


class Material(object):
    """Creates a material consisting of elements based on the Material database."""
    def __init__(self):
        self.atomDensity = 0.0
        self.density = 0.0
        self.linearCoeffExpansion = 0.0

        self.name = ''
        self.materialName = ''

        self.atomPercent = {}
        self.enrichmentDict = {}
        self.weightPercent = {}
        self.elementDict = {}

        self.elements = []
        self.zaids = []
        self.weightFraction = []
        self.enrichmentZaids = []
        self.enrichmentIsotopes = []
        self.enrichmentVector = []

    def set_material(self, material):
        self.name = material
        self.read_material(self.name)
        self.create_material_data()

    def read_material(self, material):
        """Read in the material data from the material database."""
        material_yaml_file = glob.glob(os.path.join(material_dir, material + '.yaml'))

        if not material_yaml_file:
            raise AssertionError("Material {}, not found in material database. Please create material file for {}."
                                 .format(material, material))

        with open(material_yaml_file[0], "r") as file:
            inputs = yaml.safe_load(file)
            self.name = inputs['Name']
            self.materialName = material
            self.elements = inputs['Elements']
            self.zaids = inputs['ZAIDs']
            self.weightFraction = inputs['Weight Fractions'] if 'Weight Fractions' in inputs else []
            self.enrichmentZaids = inputs['Enrichment ZAIDs'] if 'Enrichment ZAIDs' in inputs else []
            self.enrichmentIsotopes = inputs['Enrichment Isotopes'] if 'Enrichment Isotopes' in inputs else []
            self.enrichmentVector = inputs['Enrichment Vector'] if 'Enrichment Vector' in inputs else []
            self.density = inputs['Density']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']

    def create_material_data(self):
        """Create a material based on the data from the material database."""
        for num, zaid in enumerate(self.enrichmentZaids):
            enriched_isotope_dict = {}
            for isoNum, isotopes in enumerate(self.enrichmentIsotopes[num]):
                enriched_isotope_dict[isotopes] = self.enrichmentVector[num][isoNum]
            self.enrichmentDict[zaid] = enriched_isotope_dict
        for num, element in enumerate(self.elements):
            self.elementDict[self.zaids[num]] = Element.Element(element)
        self.set_elemental_enrichment()
        self.set_weight_percent()
        self.atomDensity, self.atomPercent = set_atom_percent(self.weightPercent, self.density,
                                                              self.elementDict)

    def set_elemental_enrichment(self):
        """Adjust the element's natural abundance to compensate for enrichment."""
        for elementEnrichement, zaidVector in self.enrichmentDict.items():
            for zaid, enrichmentPercent in zaidVector.items():
                self.elementDict[elementEnrichement].weightPercentDict[zaid] = enrichmentPercent

    def set_weight_percent(self, void_percent=1.0):
        """Calculates the weight percent of a material."""
        weight_total = 0.0
        for zaidNum, zaid in enumerate(self.zaids):
            for isotope, isotopeFraction in self.elementDict[zaid].weightPercentDict.items():
                if isotopeFraction != 0.0:
                    self.weightPercent[isotope] = isotopeFraction * self.weightFraction[zaidNum] * void_percent
                    weight_total += self.weightPercent[isotope]
        try:
            assert np.allclose(weight_total, 1.0 * void_percent)
        except AssertionError:
            print("Weight percent does not sum to 1.0 for {}. Check the material file.".format(self.name))

    def set_void(self, void_percent):
        self.set_weight_percent(void_percent)
        self.atomDensity, self.atomPercent = set_atom_percent(self.weightPercent, self.density,
                                                              self.elementDict)


def set_atom_percent(weight_percents, density, element_dict):
    """Converts the weight percent of a material to the atom percent and atom density."""
    atom_densities = {}
    atom_percent = {}
    for zaid, weight in weight_percents.items():
        element = str(zaid)
        if len(element) < 5:
            current_element = int(element[:1] + '000')
        else:
            current_element = int(element[:2] + '000')
        atom_densities[zaid] = weight*density * AVOGADROS_NUMBER / element_dict[current_element].molecularMassDict[zaid]
    atom_density = sum(atom_densities.values())

    for zaid, atomicDensity in atom_densities.items():
        atom_percent[zaid] = atomicDensity / atom_density
    return atom_density, atom_percent
