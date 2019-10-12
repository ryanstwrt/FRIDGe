import numpy as np
import glob
import os
import fridge.Material.Element as Element
import fridge.utilities.utilities as utilities

AVOGADROS_NUMBER = 0.6022140857
cur_dir = os.path.dirname(__file__)
material_dir = os.path.join(cur_dir, '../data/materials/')


class Material(object):
    """Creates a material consisting of elements based on the Material database."""
    def __init__(self):
        self.atomDensity = 0.0
        self.density = 0.0
        self.linearCoeffExpansion = 0.0
        self.molecularMass = 0.0

        self.name = ''
        self.materialName = ''

        self.atomPercent = {}
        self.atomDensities = {}
        self.enrichmentDict = {}
        self.weightPercent = {}
        self.elementDict = {}

        self.elements = []
        self.zaids = []
        self.weightFraction = []
        self.enrichmentZaids = []
        self.enrichmentIsotopes = []
        self.enrichmentVector = []
        self.isotopicAtomPercents = []

    def set_material(self, material):
        self.name = material
        self.read_material_data(self.name)
        self.create_material_data()

    def read_material_data(self, material):
        """Read in the material data from the material database."""
        material_yaml_file = glob.glob(os.path.join(material_dir, material + '.yaml'))

        inputs = utilities.yaml_reader(material_yaml_file, material_dir, material)
        self.name = inputs['Name']
        self.materialName = material
        self.elements = inputs['Elements']
        self.zaids = inputs['Elemental ZAIDs']
        self.weightFraction = inputs['Elemental Weight Fractions'] if 'Elemental Weight Fractions' in inputs else []
        self.enrichmentZaids = inputs['Elemental Adjustment ZAIDs'] if 'Elemental Adjustment ZAIDs' in inputs else []
        self.enrichmentIsotopes = inputs['Isotopic Adjustment ZAIDs'] if 'Isotopic Adjustment ZAIDs' in inputs else []
        self.enrichmentVector = inputs['Isotopic Weight Percents'] if 'Isotopic Weight Percents' in inputs else []
        self.isotopicAtomPercents = inputs['Isotopic Atom Densities'] if 'Isotopic Atom Densities' in inputs else []
        self.atomDensity = inputs['Atom Density'] if 'Atom Density' in inputs else 0.0
        self.density = inputs['Density'] if 'Density' in inputs else 0.0
        self.molecularMass = inputs['Molecular Mass'] if 'Molecular Mass' in inputs else 0.0
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

        if self.isotopicAtomPercents:
            self.atom_density_to_atom_percent()
            if self.density != 0.0:
                self.atom_density_to_weight_percent_density()
            elif self.molecularMass != 0.0:
                self.atom_density_to_weight_percent()
            else:
                print("Warning: Material {} does not have a molecular mass or mass density. This material cannot be smeared".format(self.name))
        else:
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
        """Adjust the atom density/atom percent of a material to account for voiding."""
        self.set_weight_percent(void_percent)
        self.atomDensity, self.atomPercent = set_atom_percent(self.weightPercent, self.density, self.elementDict)

    def atom_density_to_atom_percent(self, void_percent=1.0):
        """Calculates the atom percents of a material given a material with atom densities defined."""
        for zaidNum, zaid in enumerate(self.zaids):
            for isotope, isotopeFraction in self.elementDict[zaid].atomPercentDict.items():
                if zaid in self.isotopicAtomPercents:
                    self.atomDensities[isotope] = self.elementDict[zaid].atomPercentDict[isotope] * \
                                                  self.isotopicAtomPercents[zaid] * void_percent
                    self.atomPercent[isotope] = self.atomDensities[isotope] / self.atomDensity
                elif isotope in self.isotopicAtomPercents:
                    self.atomDensities[isotope] = self.isotopicAtomPercents[isotope] * void_percent
                    self.atomPercent[isotope] = self.atomDensities[isotope] / self.atomDensity
        assert np.allclose(sum(self.atomDensities.values()), self.atomDensity, 3)

    def atom_density_to_weight_percent(self, void_percent=1.0):
        summedWeightPercent = 0
        for zaid, atom_per in self.atomPercent.items():
            element = str(zaid)
            if len(element) < 5:
                current_element = int(element[:1] + '000')
            else:
                current_element = int(element[:2] + '000')
            try:
                self.weightPercent[zaid] = atom_per * self.elementDict[current_element].molecularMassDict[zaid] / \
                                           self.molecularMass
                summedWeightPercent += self.weightPercent[zaid]
            except ZeroDivisionError:
                pass
        for zaid, wp in self.weightPercent.items():
            self.weightPercent[zaid] = wp/summedWeightPercent

    def atom_density_to_weight_percent_density(self, void_percent=1.0):
        molecular_mass = 0
        for zaid, atom_per in self.atomPercent.items():
            element = str(zaid)
            if len(element) < 5:
                current_element = int(element[:1] + '000')
            else:
                current_element = int(element[:2] + '000')
            try:
                self.weightPercent[zaid] = self.atomDensities[zaid] * \
                                           self.elementDict[current_element].molecularMassDict[zaid] / \
                                           (self.density * AVOGADROS_NUMBER)
                molecular_mass += self.weightPercent[zaid]
            except AssertionError:
                pass
        for zaid, wp in self.weightPercent.items():
            self.weightPercent[zaid] = wp/molecular_mass
        print(molecular_mass)


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
        atom_densities[zaid] = weight*density*AVOGADROS_NUMBER / element_dict[current_element].molecularMassDict[zaid]
    atom_density = sum(atom_densities.values())

    for zaid, atomicDensity in atom_densities.items():
        atom_percent[zaid] = atomicDensity / atom_density
    return atom_density, atom_percent


def get_smeared_material(materials, void_material='', void_percent=1.0):
    """Create the material data card for a smeared material."""
    smear_material = {}
    for material, materialWeightPercent in materials.items():
        void_multiplier = 1.0
        if material == 'Void':
            pass
        else:
            base_material = Material()
            base_material.set_material(material)

            if base_material.materialName == void_material:
                void_multiplier = void_percent

            for isotope, isotopeWeightPercent in base_material.weightPercent.items():
                element = str(isotope)
                if len(element) < 5:
                    current_element = element[:1] + '000'
                else:
                    current_element = element[:2] + '000'
                current_element = int(current_element)
                try:
                    smear_material[isotope] += isotopeWeightPercent * materialWeightPercent * base_material.density \
                                              * AVOGADROS_NUMBER * void_multiplier / \
                                              base_material.elementDict[current_element].molecularMassDict[isotope]
                except KeyError:
                    smear_material[isotope] = isotopeWeightPercent * materialWeightPercent * base_material.density \
                                             * AVOGADROS_NUMBER * void_multiplier / \
                                             base_material.elementDict[current_element].molecularMassDict[isotope]
    smeared_material = Material()
    smeared_material.name = "{}".format([val for val in materials])
    smeared_material.atomDensity = sum(smear_material.values())
    smeared_atom_percent = {}
    for k, v in smear_material.items():
        smeared_atom_percent[k] = v / smeared_material.atomDensity
    smeared_material.atomPercent = smeared_atom_percent
    return smeared_material


def smear_coolant_wirewrap(info):
    """Returns a smeared material for the coolant and wire wrap."""
    height = info[0]
    fuel_radius = info[1] / 2
    wirewrap_radius = info[2] / 2
    wire_wrap_axial_pitch = info[3]
    fuel_pitch = info[4]
    coolant_material = info[5]
    clad_material = info[6]
    fuel_volume = utilities.get_cylinder_volume(fuel_radius, height)
    wire_wrap_volume = utilities.get_toroidal_volume(fuel_radius, wirewrap_radius, wire_wrap_axial_pitch, height)
    pin_hexagonal_universe_volume = utilities.get_hexagonal_prism_volume(fuel_pitch, height)
    coolant_volume = pin_hexagonal_universe_volume - fuel_volume - wire_wrap_volume
    total_coolant_wire_wrap_volume = coolant_volume + wire_wrap_volume
    wire_wrap_volume_percent = wire_wrap_volume / total_coolant_wire_wrap_volume
    coolant_volume_percent = coolant_volume / total_coolant_wire_wrap_volume
    smeared_material_dict = {clad_material: wire_wrap_volume_percent, coolant_material: coolant_volume_percent}
    return smeared_material_dict
