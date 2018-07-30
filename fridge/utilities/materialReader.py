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

    def __init__(self, material):
        self.enrichmentDict = {}
        self.isotopeDict = {}
        self.weightPercent = {}
        self.atomPercent = {}
        self.atomDensity = 0.0
        self.elementDict = {}
        self.materialName = material
        self.readMaterial(self.materialName)
        self.getMaterial()

    def readMaterial(self, material):
        material_file = glob.glob(os.path.join(material_dir, material + '.yaml'))
        with open(material_file[0], "r") as file:
            inputs = yaml.load(file)
            self.name = inputs['Name']
            self.elements = inputs['Elements']
            self.zaids = inputs['ZAIDs']
            self.weightFraction = inputs['Weight Fractions']
            self.density = inputs['Density']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']
            self.enrichmentZaids = inputs['Enrichment ZAIDs']
            self.enrichmentIsotopes = inputs['Enrichment Isotopes']
            self.enrichmentVector = inputs['Enrichment Vector']

    def getMaterial(self):
            for num, zaid in enumerate(self.enrichmentZaids):
                enrichedIsotopeDict = {}
                for isoNum, isotopes in enumerate(self.enrichmentIsotopes[num]):
                    enrichedIsotopeDict[isotopes] = self.enrichmentVector[num][isoNum]
                self.enrichmentDict[zaid] = enrichedIsotopeDict
            for num, element in enumerate(self.elements):
                self.elementDict[self.zaids[num]] = Element(element)
            self.adjustEnrichments()
            self.getWeightPercet()
            self.getAtomPercent()

    def adjustEnrichments(self):
        for elementEnrichement, zaidVector in self.enrichmentDict.items():
            for zaid, enrichmentPercent in zaidVector.items():
                self.elementDict[elementEnrichement].isotopeDict[zaid] = enrichmentPercent

    def getWeightPercet(self):
        weightTotal = 0.0
        for zaidNum, zaid in enumerate(self.zaids):
            for isotope, isotopeFraction in self.elementDict[zaid].isotopeDict.items():
                if isotopeFraction != 0.0:
                    self.weightPercent[isotope] = isotopeFraction * self.weightFraction[zaidNum]
                    weightTotal += self.weightPercent[isotope]
        assert np.allclose(weightTotal, 1.0)

    def getAtomPercent(self):
        atomDensities = {}
        atomPercentTotal = 0.0
        for zaid, weight in self.weightPercent.items():
            currentElement = str(zaid)[:2] + '000'
            currentElement = int(currentElement)
            atomDensities[zaid] = weight * self.density * AVOGADROS_NUMBER / self.elementDict[currentElement].molecularMassDict[zaid]
            self.atomDensity += atomDensities[zaid]
        for zaid, atomicDensity in atomDensities.items():
            self.atomPercent[zaid] = atomicDensity / self.atomDensity
            atomPercentTotal += self.atomPercent[zaid]
        assert np.allclose(atomPercentTotal, 1.0)


class Element(object):

    def __init__(self, element):
        element_file = glob.glob(os.path.join(element_dir, element + '.yaml'))
        with open(element_file[0], "r") as file:
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
