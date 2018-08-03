import FRIDGe.fridge.utilities.materialReader as materialReader
import numpy as np
import pandas as pd
import math
import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")

class Assembly(object):

    def __init__(self, assemblyInformation):
        self.assemblyType = assemblyInformation[0]
        self.position = assemblyInformation[1]
        self.assemblyReader(self.assemblyType)
        self.getPosition(self.position, self.assemblyPitch)
        self.getAssembly()

    def getPosition(self, position, pitch):
        ring = int(position[:2]) - 1
        hextant = position[2]
        assemblyNum = int(position[3:]) - 1
        zPosition = 0.0

        if hextant == 'A':
            xPosition = -ring*math.sqrt(pow(pitch,2)+(pow(pitch/2,2)))
            yPosition = ring*pow(pitch/2,2)+pitch*assemblyNum
        elif hextant == 'B':
            xPosition = pitch*assemblyNum
            yPosition = ring*pitch + pitch/2*assemblyNum
        elif hextant == 'C':
            xPosition = (ring) * math.sqrt((pow(pitch, 2) - pow(pitch / 2, 2)))
            yPosition = (ring) * pow(pitch / 2, 2) - pitch * assemblyNum
        elif hextant == 'D':
            xPosition = -ring * math.sqrt(pow(pitch, 2) + (pow(pitch / 2,2)))
            yPosition = -ring * pow(pitch / 2, 2) - pitch * assemblyNum
        elif hextant == 'E':
            xPosition = -pitch*assemblyNum
            yPosition = ring*pitch - pitch/2*assemblyNum
        elif hextant == 'F':
            xPosition = -(ring)*math.sqrt((pow(pitch,2)-pow(pitch/2,2)))
            yPosition = (ring)*pow(pitch/2,2)+pitch*assemblyNum

        self.position = [xPosition, yPosition, zPosition]


    def getReflectorInfo(self, inputs):
        self.reflectorHeight = float(inputs['Fuel Reflector Height'])
        reflectorSmear = [float(i) for i in inputs['Smear']]
        reflectorMaterial = inputs['Material']
        self.reflectorMaterial = {}
        for num, material in enumerate(reflectorMaterial):
            self.reflectorMaterial[material] = reflectorSmear[num]

    def getAssemblyInfo(self, inputs):
        self.pinsPerAssembly = float(inputs['Pins Per Assembly'])
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductThickness = float(inputs['Duct Thickness'])
        self.assemblGap = float(inputs['Assembly Gap'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat'])
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolant = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']


class FuelAssembly(Assembly):

    def getAssembly(self):
        self.fuel = FuelPin([[1, 1, 1, '5Pu22U10Zr', '82C', self.position], [self.fuelDiameter, self.fuelHeight, self.fuelPitch]])
        #self.bond = FuelBond([[1, 1, 1, 'Liquid_Sodium', '82C', self.position], [self.fuelDiameter, self.fuelHeight, self.fuelPitch])

    def assemblyReader(self, assemblyType):
        assembly_yaml_file = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))

        if assembly_yaml_file == []:
            raise AssertionError('No assembly type named {}. Change your assembly type to a previously created assembly, '
                  'or create a new assembly.'.format(assemblyType))


        with open(assembly_yaml_file[0], "r") as mat_file:
            inputs = yaml.load(mat_file)
            self.getFuelRegionInfo(inputs)
            self.getPlenumRegionInfo(inputs)
            self.getReflectorInfo(inputs)
            self.getAssemblyInfo(inputs)

    def getFuelRegionInfo(self, inputs):
        self.cladThickness = float(inputs['Clad Thickness'])
        try:
            self.fuelDiameter = float(inputs["Pin Diameter"])
        except AssertionError:
            self.fuelDiameter = 2*math.sqrt(float(inputs['Fuel Smear']))
        self.fuelPitch = float(inputs['Pitch'])
        self.wireWrapDiameter = float(inputs['Wire Wrap Diameter'])
        self.fuelHeight = float(inputs['Fuel Height'])
        self.fuelMaterial = inputs['Fuel']
        self.cladMaterial = inputs['Clad']
        self.bondMaterial = inputs['Bond']

    def getPlenumRegionInfo(self, inputs):
        self.plenumHeight = float(inputs['Plenum Height'])
        plenumSmear = [float(i) for i in inputs['Plenum Smear']]
        plenumMaterial = inputs["Plenum Material"]
        self.plenumMaterial = {}
        for num, material in enumerate(plenumMaterial):
            self.plenumMaterial[material] = plenumSmear[num]

    def getAssemblyMCNP(self):
        self.fuel = FuelPin([[1, 1, 1, '5Pu22U10Zr', '900K'], [self.position]])

class Unit(object):
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][1] + 1
        self.cellNum = unitInfo[0][2] + 1
        self.materialXCLibrary = unitInfo[0][4]
        self.position = unitInfo[0][5]
        self.materialNum = self.cellNum
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])
        self.getSurfaceCard([1])
        getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)


    def getMaterialCard(self, material):
        self.material = materialReader.Material(material)

    def getSurfaceCard(self, unitType):
        pass


class FuelPin(Unit):
    def makeComponent(self, pinInfo):
        self.radius = pinInfo[0]/2
        self.height = pinInfo[1]
        self.pitch = pinInfo[2]
        surfaceComment = "$Fuel Pin"
        cellComment = "$Fuel Pin"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum, cellComment)


class FuelBond(Unit):
    def __init__(self, bondInfo, fuelPin):
        self.radius = bondInfo[0]/2
        self.innerRadius = fuelPin.radius


def getRCC(radius, height, position, surfaceNum, comment):
    surfaceCard = "{} RCC {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], position[2], height, radius, comment)
    assert len(surfaceCard) < 80
    return surfaceCard


def getSingleCell(cellNum, matNum, density, surfaceNum, comment):
    cellCard = "{} {} {} -{} imp:n=1  {}".format(cellNum, matNum, density, surfaceNum, comment)
    assert len(cellCard) < 80
    return cellCard

def getMaterialCard(material, xc, matNum):
    materialCard = "c Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name, material.density, matNum)
    for isotope, atomDensity in material.atomPercent.items():
        materialCard += "      {}.{} {}\n".format(isotope, xc, atomDensity)
    return materialCard

assembly = FuelAssembly(['A271', '01A01'])
fuelPin = assembly.fuel
print(fuelPin.surfaceCard)
print(fuelPin.cellCard)

