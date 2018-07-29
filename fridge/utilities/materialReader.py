import numpy as np
import glob
import os
import yaml

AVOGADROS_NUMBER = 0.6022140857
# Requirements for the material reader
txt_ext = ".txt"
cur_dir = os.path.dirname(__file__)
element_dir = os.path.join(cur_dir, '../data/CotN/')
material_dir = os.path.join(cur_dir, '../data/materials/')


class Material(object):

    def __init__(self):
        pass


    def getMaterial(self, material):
        material_file = glob.glob(os.path.join(material_dir, material + '.yaml'))
        with open(material_file[0], "r") as file:
            inputs = yaml.load(file)
            self.name = inputs['Name']
            self.elements = inputs['Elements']
            self.zaids = inputs['ZAIDs']
            self.weightFractions = inputs['Weight Fractions']
            self.density = inputs['Density']
            self.linearCoeffExpansion = inputs['Linear Coefficient of Expansion']
            self.enrichmentZaids = inputs['Enrichment ZAIDs']
            self.enrichmentIsotopes = inputs['Enrichment Isotopes']
            self.enrichmentVector = inputs['Enrichment Vector']
            self.enrichmentDict = {}
            for num, zaid in enumerate(self.enrichmentZaids):
                isotopeDict = {}
                for isoNum, isotopes in enumerate(self.enrichmentIsotopes[num]):
                    isotopeDict[isotopes] = self.enrichmentVector[num][isoNum]
                self.enrichmentDict[zaid] = isotopeDict
            self.elementDict = {}
            for num, element in enumerate(self.elements):
                self.elementDict[self.zaids[num]] = Element(element)

    def adjustEnrichments(self):
        for elementEnrichement, zaidVector in self.enrichmentDict.items():
            for zaid, enrichmentPercent in zaidVector.items():
                self.elementDict[elementEnrichement].isotopeDict[zaid] = enrichmentPercent

    def getWeightPercet(self):
        pass


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
            for num, isotopes in enumerate(self.isotopes):
                self.isotopeDict[isotopes] = self.abundance[num]

test = Material()
element = Element('C')
test.getMaterial('5Pu22U10Zr')
test.adjustEnrichments()


