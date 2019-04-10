import numpy as np
import glob
import os
import yaml

AVOGADROS_NUMBER = 0.6022140857
# Requirements for the material reader
cur_dir = os.path.dirname(__file__)
element_dir = os.path.join(cur_dir, '../data/CotN/')
material_dir = os.path.join(cur_dir, '../data/materials/')


class Material(object):

    def __init__(self):
        self.enrichmentDict = {}
        self.isotopeDict = {}
        self.weightPercent = {}
        self.atomPercent = {}
        self.atomDensity = 0.0
        self.elementDict = {}
        self.name = ''
        self.elements = []
        self.zaids = []
        self.weightFraction = []
        self.density = 0.0
        self.linearCoeffExpansion = 0.0
        self.enrichmentZaids = []
        self.enrichmentIsotopes = []
        self.enrichmentVector = []

    def setMaterial(self, material):
        self.name = material
        self.readMaterial(self.name)
        self.getMaterial()

    def readMaterial(self, material):
        materialFile = glob.glob(os.path.join(material_dir, material + '.yaml'))

        if not materialFile:
            raise AssertionError("Material {}, not found in material database. Please create material file for {}."
                                 .format(material, material))

        with open(materialFile[0], "r") as file:
            inputs = yaml.load(file)
            self.name = inputs['Name']
            self.elements = inputs['Elements']
            self.zaids = inputs['ZAIDs']
            self.weightFraction = inputs['Weight Fractions']
            self.density = inputs['Density']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']
            self.enrichmentZaids = inputs['Enrichment ZAIDs'] if 'Enrichment ZAIDs' in inputs else []
            self.enrichmentIsotopes = inputs['Enrichment Isotopes'] if 'Enrichment Isotopes' in inputs else []
            self.enrichmentVector = inputs['Enrichment Vector'] if 'Enrichment Vector' in inputs else []

    def getMaterial(self):
            for num, zaid in enumerate(self.enrichmentZaids):
                enrichedIsotopeDict = {}
                for isoNum, isotopes in enumerate(self.enrichmentIsotopes[num]):
                    enrichedIsotopeDict[isotopes] = self.enrichmentVector[num][isoNum]
                self.enrichmentDict[zaid] = enrichedIsotopeDict
            for num, element in enumerate(self.elements):
                self.elementDict[self.zaids[num]] = Element(element)
            self.adjustEnrichments()
            self.getWeightPercent()
            self.atomDensity, self.atomPercent = getAtomPercent(self.weightPercent, self.density,
                                                                self.elementDict, self.name)

    def adjustEnrichments(self):
        for elementEnrichement, zaidVector in self.enrichmentDict.items():
            for zaid, enrichmentPercent in zaidVector.items():

                self.elementDict[elementEnrichement].isotopeDict[zaid] = enrichmentPercent

    def getWeightPercent(self):
        weightTotal = 0.0
        for zaidNum, zaid in enumerate(self.zaids):
            for isotope, isotopeFraction in self.elementDict[zaid].isotopeDict.items():
                if isotopeFraction != 0.0:
                    self.weightPercent[isotope] = isotopeFraction * self.weightFraction[zaidNum]
                    weightTotal += self.weightPercent[isotope]
        try:
            assert np.allclose(weightTotal, 1.0)
        except AssertionError:
            print("Weight percent does not sum to 1.0 for {}. Check the material file.".format(self.name))


def getAtomPercent(weightPercents, density, elementDict, name):
    atomDensities = {}
    atomPercent = {}
    for zaid, weight in weightPercents.items():
        element = str(zaid)
        if len(element) < 5:
            currentElement = int(element[:1] + '000')
        else:
            currentElement = int(element[:2] + '000')
        atomDensities[zaid] = weight * density * AVOGADROS_NUMBER / elementDict[currentElement].molecularMassDict[zaid]
    atomDensity = sum(atomDensities.values())

    for zaid, atomicDensity in atomDensities.items():
        atomPercent[zaid] = atomicDensity / atomDensity
    return atomDensity, atomPercent


class Element(object):

    def __init__(self, element):
        elementFile = glob.glob(os.path.join(element_dir, element + '.yaml'))

        if not elementFile:
            self.error = "Element {}, not found in Chart of the Nuclide Database. " \
                                 "Please create element file for {}.".format(element, element)
            raise AssertionError(self.error)

        with open(elementFile[0], "r") as file:
            inputs = yaml.load(file)
            self.name = inputs['Name']
            self.zaid = inputs['ZAID']
            self.isotopes = inputs['Isotopes']
            self.molecularMass = inputs['Mass']
            self.density = inputs['Density']
            self.abundance = inputs['Abundance']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']
            self.isotopeDict = {}
            self.molecularMassDict = {}
            for num, isotope in enumerate(self.isotopes):
                self.isotopeDict[isotope] = self.abundance[num]
            for num, isotope in enumerate(self.isotopes):
                self.molecularMassDict[isotope] = self.molecularMass[num]
