import FRIDGe.fridge.utilities.materialReader as materialReader
from decimal import Decimal
import numpy as np
import math
import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")


class Assembly(object):

    def __init__(self, assemblyInformation):
        self.assemblyDesignation = assemblyInformation[0]
        self.assemblyPosition = assemblyInformation[1]
        self.globalVars = assemblyInformation[2]
        self.universe = self.globalVars.universe
        self.cellNum = self.globalVars.cellNumber
        self.surfaceNum = self.globalVars.surfaceNumber
        self.materialNum = self.globalVars.materialNumber
        self.assemblyType = ''
        self.pinsPerAssembly = 0
        self.assemblyPitch = 0
        self.ductInnerFlatToFlat = 0
        self.ductOuterFlatToFlat = 0
        self.ductOuterFlatToFlatUniverse = 0
        self.assemblyGap = 0
        self.assemblyHeight = 0
        self.coolantMaterial = ''
        self.assemblyMaterial = ''

    def getAssemblyInfo(self, inputs):
        self.pinsPerAssembly = float(inputs['Pins Per Assembly'])
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat'])
        self.ductOuterFlatToFlat = self.ductInnerFlatToFlat + 2*float(inputs['Duct Thickness'])
        self.ductOuterFlatToFlatUniverse = self.ductOuterFlatToFlat * 1.00005
        self.assemblyGap = float(inputs['Assembly Gap'])
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolantMaterial = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']

    def updateIdentifiers(self):
        self.cellNum += 1
        self.surfaceNum += 1
        self.materialNum += 1


def assemblyTypeReader(assemblyYamlFile):
    with open(assemblyYamlFile[0], "r") as mat_file:
        inputs = yaml.load(mat_file)
        assemblyType = inputs['Assembly Type']
    return assemblyType


def getAssemblyLocation(assemblyType):
    assemblyYamlFile = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))

    if not assemblyYamlFile:
        raise AssertionError(
            'No assembly type named {}. Change your assembly type to a previously created assembly, '
            'or create a new assembly.'.format(assemblyType))
    return assemblyYamlFile


class FuelAssembly(Assembly):

    def __init__(self, assemblyInformation):
        super().__init__(assemblyInformation)
        self.assemblyUniverse = 0
        self.pinUniverse = 0
        self.fuel = None
        self.bond = None
        self.clad = None
        self.coolant = None
        self.blankUniverse = None
        self.blankCoolant = None
        self.latticeUniverse = None
        self.fuelUniverse = None
        self.innerDuct = None
        self.duct = None
        self.plenum = None
        self.upperReflector = None
        self.lowerReflector = None
        self.upperSodium = None
        self.lowerSodium = None
        self.assemblyShell = None
        self.upperReflectorPosition = []
        self.lowerReflectorPosition = []
        self.everythingElse = None

        self.position = []
        self.cladOD = 0
        self.cladID = 0
        self.fuelDiameter = 0
        self.fuelPitch = 0
        self.wireWrapDiameter = 0
        self.fuelHeight = 0
        self.fuelMaterial = ''
        self.cladMaterial = ''
        self.bondMaterial = ''

        self.plenumHeight = 0
        self.plenumMaterial = ''
        self.plenumPosition = []

        self.reflectorHeight = 0
        self.reflectorMaterial = ''

        assemblyYamlFile = getAssemblyLocation(self.assemblyDesignation)
        self.setAssembly(assemblyYamlFile)
        self.getAssembly()

    def setAssembly(self, assemblyYamlFile):
        with open(assemblyYamlFile[0], "r") as mat_file:
            inputs = yaml.load(mat_file)
            self.getAssemblyInfo(inputs)
            self.getFuelRegionInfo(inputs)
            self.getPlenumRegionInfo(inputs)
            self.getReflectorInfo(inputs)

    def getAssembly(self):
        self.assemblyUniverse = self.universe
        self.universe +=1
        self.pinUniverse = self.universe
        self.fuel = FuelPin([[self.universe, self.cellNum, self.surfaceNum, self.fuelMaterial, '82C',
                              self.position, self.materialNum], [self.fuelDiameter, self.fuelHeight]])
        self.updateIdentifiers()
        self.bond = FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, '82C',
                               self.position, self.materialNum], [self.cladID, self.fuelHeight, self.fuel.surfaceNum]])
        self.updateIdentifiers()
        self.clad = FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, '82C',
                               self.position, self.materialNum], [self.cladOD, self.fuelHeight, self.bond.surfaceNum]])
        self.updateIdentifiers()
        self.coolant = FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                     self.position, self.materialNum], [self.fuelPitch, self.fuelHeight, self.clad.surfaceNum]])
        self.updateIdentifiers()
        self.universe += 1
        self.blankUniverse = self.universe
        self.blankCoolant = BlankCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                           self.position, self.materialNum], [self.fuelPitch, self.fuelHeight, self.coolant.surfaceNum]])
        self.updateIdentifiers()
        self.universe += 1
        self.latticeUniverse = self.universe
        self.fuelUniverse = FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly, self.cellNum,
                                          self.blankCoolant.cellNum, self.latticeUniverse])
        self.updateIdentifiers()
        self.innerDuct = InnerDuct([self.universe, self.cellNum, self.surfaceNum, self.assemblyUniverse,
                                    self.latticeUniverse, self.position, self.ductInnerFlatToFlat, self.fuelHeight])
        self.updateIdentifiers()
        self.duct = Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                           self.position, self.materialNum], [self.ductOuterFlatToFlatUniverse, self.fuelHeight, self.innerDuct.surfaceNum]])
        self.updateIdentifiers()
        self.plenum = Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.plenumMaterial, '82C',
                              self.plenumPosition, self.materialNum], [self.ductOuterFlatToFlatUniverse, self.plenumHeight], 'plenum'])
        self.updateIdentifiers()
        self.upperReflectorPosition = self.position
        self.upperReflectorPosition[2] += self.fuelHeight * 1.01 + self.plenumHeight
        self.upperReflector = Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.reflectorMaterial, '82C',
                                      self.position, self.materialNum], [self.ductOuterFlatToFlatUniverse, self.reflectorHeight], 'upper Reflector'])

        self.updateIdentifiers()
        self.lowerReflectorPosition = self.position
        self.lowerReflectorPosition[2] = -self.reflectorHeight
        self.lowerReflector = Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.reflectorMaterial, '82C',
                                      self.position, self.materialNum],[self.ductOuterFlatToFlatUniverse, self.reflectorHeight], 'lower Reflector'])
        self.updateIdentifiers()
        self.assemblyShell = OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C', self.materialNum],
                                         [self.reflectorHeight, self.fuelHeight, self.plenumHeight, self.assemblyHeight, self.ductOuterFlatToFlat, self.assemblyPosition]])

        self.updateIdentifiers()
        self.lowerSodium = LowerSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                              self.position, self.materialNum], [self.assemblyShell, self.ductOuterFlatToFlatUniverse]])

        self.updateIdentifiers()
        self.upperSodium = UpperSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                              self.position, self.materialNum], [self.assemblyShell, self.ductOuterFlatToFlatUniverse]])

        if 'Single' in self.globalVars.input_type:
            self.updateIdentifiers()
            self.everythingElse = EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])

    def getFuelRegionInfo(self, inputs):
        self.position = getPosition(self.assemblyPosition, self.assemblyPitch, 0.0)
        self.cladOD = float(inputs['Pin Diameter'])
        self.cladID = self.cladOD - 2*float(inputs['Clad Thickness'])
        try:
            self.fuelDiameter = float(inputs["Fuel Diameter"])
        except KeyError:
            self.fuelDiameter = math.sqrt(float(inputs['Fuel Smear'])) * self.cladID
        self.fuelPitch = float(inputs['Pitch'])
        self.wireWrapDiameter = float(inputs['Wire Wrap Diameter'])
        self.fuelHeight = float(inputs['Fuel Height'])
        self.fuelMaterial = inputs['Fuel']
        self.cladMaterial = inputs['Clad']
        self.bondMaterial = inputs['Bond']

    def getPlenumRegionInfo(self, inputs):
        self.plenumHeight = float(inputs['Plenum Height'])
        self.plenumPosition = getPosition(self.assemblyPosition, self.assemblyPitch, self.fuelHeight * 1.01)
        plenumSmear = [float(i) for i in inputs['Plenum Smear']]
        plenumMaterial = inputs["Plenum Material"]
        self.plenumMaterial = {}
        for num, material in enumerate(plenumMaterial):
            self.plenumMaterial[material] = plenumSmear[num]

    def getReflectorInfo(self, inputs):
        self.reflectorHeight = float(inputs['Fuel Reflector Height'])
        reflectorSmear = [float(i) for i in inputs['Smear']]
        reflectorMaterial = inputs['Material']
        self.reflectorMaterial = {}
        for num, material in enumerate(reflectorMaterial):
            self.reflectorMaterial[material] = reflectorSmear[num]

    def getAssemblyMCNP(self):
        self.fuel = FuelPin([[1, 1, 1, '5Pu22U10Zr', '900K'], [self.position]])

class Unit(object):
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][1]
        self.cellNum = unitInfo[0][2]
        self.materialXCLibrary = unitInfo[0][4]
        self.position = unitInfo[0][5]
        self.materialNum = unitInfo[0][6]
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def getMaterialCard(self, materialName):
        self.material = materialReader.Material()
        self.material.setMaterial(materialName)
        self.materialCard = getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)


class FuelPin(Unit):
    def makeComponent(self, pinInfo):
        self.radius = pinInfo[0]/2
        self.height = pinInfo[1]
        surfaceComment = "$Pin: Fuel"
        cellComment = "$Pin: Fuel"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum, self.universe, cellComment)


class FuelBond(Unit):
    def makeComponent(self, bondInfo):
        self.radius = bondInfo[0]/2
        self.height = bondInfo[1]*1.01
        self.fuelSurfaceNum = bondInfo[2]
        surfaceComment = "$Pin: Bond - 1% higher than fuel"
        cellComment = "$Pin: Bond"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.fuelSurfaceNum, self.surfaceNum, self.universe, cellComment)


class FuelClad(Unit):
    def makeComponent(self, cladInfo):
        self.radius = cladInfo[0]/2
        self.height = cladInfo[1]*1.01
        self.bondSurfaceNum = cladInfo[2]
        surfaceComment = "$Pin: Clad - 1% higher than fuel"
        cellComment = "$Pin: Clad"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.bondSurfaceNum, self.surfaceNum, self.universe, cellComment)

class FuelCoolant(Unit):
    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0]
        self.height = coolantInfo[1] * 1.01
        self.cladSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Coolant - 1% higher than fuel"
        cellComment = "$Pin: Wirewrap + Coolant"
        self.surfaceCard = getRHPRotated(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getOutsideCell(self.cellNum, self.materialNum, self.material.density,
                                          self.cladSurfaceNum, self.universe, cellComment)


class BlankCoolant(Unit):
    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0] / 2
        self.height = coolantInfo[1] * 1.01
        self.blankCoolantSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Blank Pin - 1% higher than fuel"
        cellComment = "$Pin: Blank Pin Coolant"
        self.surfaceCard = getRHPRotated(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density,
                                      self.blankCoolantSurfaceNum, self.universe, cellComment)


class FuelUniverse(Unit):
    def __init__(self, fuelUniverseInfo):
        self.fuelUniverse = fuelUniverseInfo[0]
        self.blankUniverse = fuelUniverseInfo[1]
        self.numPins = fuelUniverseInfo[2]
        self.cellNum = fuelUniverseInfo[3]
        self.blankCellNum = fuelUniverseInfo[4]
        self.latticeUniverse = fuelUniverseInfo[5]
        self.cellCard = self.getCellCard()

    def getCellCard(self):
        cellCard = "{} 0 -{} lat=2 u={} imp:n=1\n".format(self.cellNum, self.blankCellNum, self.latticeUniverse)
        rings = int(max(np.roots([1, -1, -2*(self.numPins-1)/6])))
        lattice_array = np.zeros((rings * 2 + 1, rings * 2 + 1))
        for x in range(rings * 2 + 1):
            for y in range(rings * 2 + 1):
                if x == 0 or x == 2 * rings:
                    lattice_array[x][y] = self.blankUniverse
                elif x < (rings + 1):
                    if y < (rings + 1 - x) or y == (2 * rings):
                        lattice_array[x][y] = self.blankUniverse
                    else:
                        lattice_array[x][y] = self.fuelUniverse
                else:
                    if y > (2 * rings - (x - rings + 1)) or y == 0:
                        lattice_array[x][y] = self.blankUniverse
                    else:
                        lattice_array[x][y] = self.fuelUniverse

        cellCard += "     fill=-{}:{} -{}:{} 0:0\n     ".format(rings,rings,rings,rings)
        for row in lattice_array:
            for lat_iter, element in enumerate(row):
                if (lat_iter+1) % 10 == 0:
                    cellCard += " {}\n     ".format(int(element))
                else:
                    cellCard += " {}".format(int(element))
        return cellCard


class InnerDuct(Unit):
    def __init__(self, ductInfo):
        self.universe = ductInfo[0]
        self.cellNum = ductInfo[1]
        self.surfaceNum = ductInfo[2]
        self.assemblyUniverse = ductInfo[3]
        self.latticeUniverse = ductInfo[4]
        self.position = ductInfo[5]
        self.flat2flat = ductInfo[6]
        self.height = ductInfo[7] * 1.01
        self.makeComponent()

    def makeComponent(self):
        surfaceComment = "$Assembly: Duct Inner Surface"
        cellComment = "$Assembly: Inner Portion of Assembly"
        self.surfaceCard = getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getFuelLatticeCell(self.cellNum, self.surfaceNum, self.assemblyUniverse, self.latticeUniverse, cellComment)


class Duct(Unit):
    def makeComponent(self, ductInfo):
        self.flat2flat = ductInfo[0]
        self.height = ductInfo[1] * 1.01
        self.innerSurfaceNum = ductInfo[2]
        surfaceComment = "$Assembly:Duct Outer Surface"
        cellComment = "$Assembly: Assembly Duct"
        self.surfaceCard = getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.innerSurfaceNum,
                                          self.surfaceNum, self.universe, cellComment)


class Smear(Unit):
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][1]
        self.cellNum = unitInfo[0][2]
        self.materialXCLibrary = unitInfo[0][4]
        self.material = unitInfo[0][3]
        self.position = unitInfo[0][5]
        self.materialNum = unitInfo[0][6]
        self.smearName = unitInfo[2]
        self.material = getSmearedMaterial(self.material, self.materialXCLibrary, self.materialNum)
        self.makeComponent(unitInfo[1])
        self.getMaterialCard(self.material)

    def makeComponent(self, ductInfo):
        self.flat2flat = ductInfo[0]
        self.height = ductInfo[1]
        surfaceComment = "$Assembly: {}".format(self.smearName)
        cellComment = "$Assembly: {}".format(self.smearName)
        self.surfaceCard = getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density,
                                          self.surfaceNum, self.universe, cellComment)

    def getMaterialCard(self, materialName):
        self.materialCard = getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)


class OuterShell(Unit):
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][2]
        self.cellNum = unitInfo[0][1]
        self.materialXCLibrary = unitInfo[0][4]
        self.materialNum = unitInfo[0][5]
        self.getMaterialCard(unitInfo[0][3])
        self.reflectorHeight = unitInfo[1][0]
        self.fuelHeight = unitInfo[1][1] * 1.01
        self.plenumHeight = unitInfo[1][2]
        self.assemblyHeight = unitInfo[1][3]
        self.pitch = unitInfo[1][4]
        self.assemblyPosition = unitInfo[1][5]
        self.definedHeight = 2 * self.reflectorHeight + self.fuelHeight + self.plenumHeight
        self.excessNaHeight = (self.assemblyHeight - self.definedHeight) / 2
        self.positionBottomAssembly = getPosition(self.assemblyPosition, self.pitch, -(self.reflectorHeight + self.excessNaHeight))
        self.positionTopUpperReflector = getPosition(self.assemblyPosition, self.pitch, self.definedHeight - self.reflectorHeight)
        self.makeComponent()

    def makeComponent(self):
        surfaceComment = "$Assembly: Full Assembly Surface"
        cellComment = "$Assembly"
        self.surfaceCard = getRHP(self.pitch, self.assemblyHeight, self.positionBottomAssembly, self.surfaceNum, surfaceComment)
        self.cellCard = getAssemblyUniverseCell(self.surfaceNum, self.cellNum, self.universe, cellComment)

class LowerSodium(Unit):
    def makeComponent(self, lowerSodiumInfo):
        outerShell = lowerSodiumInfo[0]
        flatToFlatUniverse = lowerSodiumInfo[1]
        surfaceComment = "$Assembly: Lower Sodium"
        cellComment = "$Assembly: Lower Sodium"
        self.surfaceCard = getRHP(flatToFlatUniverse, outerShell.excessNaHeight, outerShell.positionBottomAssembly, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum, self.universe, cellComment)


class UpperSodium(Unit):

    def makeComponent(self, upperSodiumInfo):
        outerShell = upperSodiumInfo[0]
        flatToFlatUniverse = upperSodiumInfo[1]
        surfaceComment = "$Assembly: Upper Sodium"
        cellComment = "$Assembly: Upper Sodium"
        self.surfaceCard = getRHP(flatToFlatUniverse, outerShell.excessNaHeight, outerShell.positionTopUpperReflector,  self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum, self.universe, cellComment)


class EveryThingElse(Unit):

    def __init__(self, unitInfo):
        self.cellNum = unitInfo[1]
        self.assemblySurfaceNum = unitInfo[0]
        self.makeComponent()

    def makeComponent(self):
        cellComment = "$Assembly: Outside Assembly"
        self.cellCard = getEverythingElseCard(self.assemblySurfaceNum, self.cellNum, cellComment)


def getRCC(radius, height, position, surfaceNum, comment):
    surfaceCard = "{} RCC {} {} {} 0 0 {} {} {}".format(surfaceNum, position[0], position[1], round(position[2], 5), round(height, 5) , round(radius, 5), comment)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHP(pitch, height, position, surfaceNum, comment):
    surfaceCard = "{} RHP {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5), round(height, 5), round(pitch, 5), comment)
    print(surfaceCard)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getRHPRotated(pitch, height, position, surfaceNum, comment):
    surfaceCard = "{} RHP {} {} {} 0 0 {} 0 {} 0 {}".format(surfaceNum, position[0], position[1], round(position[2], 5), round(height, 5), round(pitch, 5), comment)
    print(surfaceCard)
    assert (len(surfaceCard) - len(comment)) < 80
    return surfaceCard


def getSingleCell(cellNum, matNum, density, surfaceNum, universe, comment):
    cellCard = "{} {} {} -{} u={} imp:n=1  {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getConcentricCell(cellNum, matNum, density, innerSurface, outerSurface, universe, comment):
    cellCard = "{} {} {} {} -{} u={} imp:n=1  {}".format(cellNum, matNum, round(density, 5), innerSurface, outerSurface, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getOutsideCell(cellNum, matNum, density, surfaceNum, universe, comment):
    cellCard = "{} {} {} {} u={} imp:n=1  {}".format(cellNum, matNum, round(density, 5), surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getFuelLatticeCell(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment):
    cellCard = "{} 0 -{} u={} fill={} imp:n=1 {}".format(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getAssemblyUniverseCell(cellNum, surfaceNum, universe, comment):
    cellCard = "{} 0 -{} fill={} imp:n=1 {}".format(cellNum, surfaceNum, universe, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getEverythingElseCard(cellNum, surfaceNum, comment):
    cellCard = "{} 0 {} imp:n=0 {}".format(cellNum, surfaceNum, comment)
    assert (len(cellCard) - len(comment)) < 80
    return cellCard


def getMaterialCard(material, xc, matNum):
    materialCard = "\nc Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name, material.density, matNum)
    i = 0
    for isotope, atomDensity in material.atomPercent.items():
        if i == 3:
            materialCard += "\n    ".format(isotope, xc, Decimal(atomDensity))
            i = 0
        materialCard += " {}.{} {:.4E}".format(isotope, xc, Decimal(atomDensity))
        i += 1
    return materialCard


def getSmearedMaterial(materials, xc, matNum):
    smearMaterial = {}
    avogadros = materialReader.AVOGADROS_NUMBER
    for material, materialWeightPercent in materials.items():
        if material == 'Void':
            pass
        else:
            materialClass = materialReader.Material()
            materialClass.setMaterial(material)
            for isotope, isotopeWeightPercent in materialClass.weightPercent.items():
                element = str(isotope)
                if len(element) < 5:
                    currentElement = element[:1] + '000'
                else:
                    currentElement = element[:2] + '000'
                currentElement = int(currentElement)
                try:
                    smearMaterial[isotope] += isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                              * avogadros / materialClass.elementDict[currentElement].molecularMassDict[isotope]
                except KeyError:
                    smearMaterial[isotope] = isotopeWeightPercent * materialWeightPercent * materialClass.density \
                                             * avogadros / materialClass.elementDict[currentElement].molecularMassDict[isotope]
    newMaterial = materialReader.Material()
    newMaterial.name = "{}".format([val for val in materials])
    newMaterial.atomPercent = smearMaterial
    newMaterial.density = sum(smearMaterial.values())
    return newMaterial


def getPosition(position, pitch, zPosition):
    ring = int(position[:2]) - 1
    hextant = position[2]
    assemblyNum = int(position[3:]) - 1
    x = 0
    y = 0

    if hextant == 'A':
        x = -ring * math.sqrt(pow(pitch, 2) + (pow(pitch/2, 2)))
        y = ring * pow(pitch/2, 2) + pitch*assemblyNum
    elif hextant == 'B':
        x = pitch*assemblyNum
        y = ring*pitch + pitch/2*assemblyNum
    elif hextant == 'C':
        x = ring * math.sqrt((pow(pitch, 2) - pow(pitch / 2, 2)))
        y = ring * pow(pitch / 2, 2) - pitch * assemblyNum
    elif hextant == 'D':
        x = -ring * math.sqrt(pow(pitch, 2) + (pow(pitch / 2, 2)))
        y = -ring * pow(pitch / 2, 2) - pitch * assemblyNum
    elif hextant == 'E':
        x = -pitch*assemblyNum
        y = ring*pitch - pitch/2*assemblyNum
    elif hextant == 'F':
        x = -ring * math.sqrt((pow(pitch, 2)-pow(pitch/2, 2)))
        y = ring * pow(pitch/2, 2)+pitch*assemblyNum
    return [x, y, zPosition]
