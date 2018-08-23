import FRIDGe.fridge.utilities.materialReader as materialReader
import FRIDGe.fridge.driver.global_variables as gb
import numpy as np
import math
import glob
import os
import yaml

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/assembly")

class Assembly(object):

    def __init__(self, assemblyInformation):
        self.assemblyType = assemblyInformation[0]
        self.assemblyPosition = assemblyInformation[1]
        globalVars = assemblyInformation[2]
        self.universe = globalVars.universe
        self.cellNum = globalVars.cellNumber
        self.surfaceNum = globalVars.surfaceNumber
        self.materialNum = globalVars.materialNumber
        self.assemblyReader(self.assemblyType)
        self.getAssembly()

    def getPosition(self, position, pitch, zPosition):
        ring = int(position[:2]) - 1
        hextant = position[2]
        assemblyNum = int(position[3:]) - 1

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

        return [xPosition, yPosition, zPosition]

    def getAssemblyInfo(self, inputs):
        self.pinsPerAssembly = float(inputs['Pins Per Assembly'])
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat'])
        self.ductOuterFlatToFlat = self.ductInnerFlatToFlat + 2*float(inputs['Duct Thickness'])
        self.assemblGap = float(inputs['Assembly Gap'])
        self.assemblyHeight = float(inputs['Assembly Height'])
        self.coolantMaterial = inputs['Coolant']
        self.assemblyMaterial = inputs['Assembly Material']

    def updateIdentifiers(self):
        self.cellNum+=1
        self.surfaceNum+=1
        self.materialNum+=1

class FuelAssembly(Assembly):

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
        self.clad = FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, '82C',
                               self.position, self.materialNum], [self.cladOD, self.fuelHeight, self.bond.surfaceNum]])
        self.updateIdentifiers()
        self.coolant = FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                     self.position, self.materialNum], [self.fuelPitch, self.fuelHeight, self.clad.surfaceNum]])
        self.updateIdentifiers()
        self.universe += 1
        self.blankUniverse = self.universe
        self.blankCoolant = BlankCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                           self.position, self.materialNum], [self.fuelPitch, self.fuelHeight]])
        self.universe += 1
        self.latticeUniverse = self.universe
        self.fuelUniverse = FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly, self.cellNum,
                                          self.blankCoolant.cellNum, self.latticeUniverse])
        self.updateIdentifiers()
        self.innerDuct = InnerDuct([self.universe, self.cellNum, self.surfaceNum, self.assemblyUniverse,
                                    self.pinUniverse, self.position, self.ductInnerFlatToFlat, self.fuelHeight])
        self.updateIdentifiers()
        self.duct = Duct([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                           self.position, self.materialNum], [self.ductOuterFlatToFlat, self.fuelHeight]])
        self.updateIdentifiers()
        self.plenum = Smear([[self.universe, self.cellNum, self.surfaceNum, self.plenumMaterial, '82C',
                              self.plenumPosition, self.materialNum], [self.ductOuterFlatToFlat, self.plenumHeight], 'plenum'])
        self.updateIdentifiers()
        self.upperReflectorPosition = self.position
        self.upperReflectorPosition[2] += self.fuelHeight + self.plenumHeight
        self.upperReflector = Smear([[self.universe, self.cellNum, self.surfaceNum, self.reflectorMaterial, '82C',
                                      self.position, self.materialNum], [self.ductOuterFlatToFlat, self.reflectorHeight], 'upper Reflector'])
        self.lowerReflectorPosition = self.position
        self.lowerReflectorPosition[2] -= self.reflectorHeight
        self.updateIdentifiers()
        self.lowerReflector = Smear([[self.universe, self.cellNum, self.surfaceNum, self.reflectorMaterial, '82C',
                                      self.position, self.materialNum],[self.ductOuterFlatToFlat, self.reflectorHeight], 'lower Reflector'])

    def assemblyReader(self, assemblyType):
        print(assemblyType)
        print(geo_dir)
        assemblyYamlFile = glob.glob(os.path.join(geo_dir, assemblyType + '.yaml'))

        print (assemblyYamlFile)

        if not assemblyYamlFile:
            raise AssertionError('No assembly type named {}. Change your assembly type to a previously created assembly, '
                  'or create a new assembly.'.format(assemblyType))

        with open(assemblyYamlFile[0], "r") as mat_file:
            inputs = yaml.load(mat_file)
            self.getAssemblyInfo(inputs)
            self.getFuelRegionInfo(inputs)
            self.getPlenumRegionInfo(inputs)
            self.getReflectorInfo(inputs)

    def getFuelRegionInfo(self, inputs):
        self.position = self.getPosition(self.assemblyPosition, self.assemblyPitch, 0.0)
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
        print(self.assemblyPosition, self.assemblyPitch, self.fuelHeight)

        self.plenumPosition = self.getPosition(self.assemblyPosition, self.assemblyPitch, self.fuelHeight)
        print(self.plenumPosition)
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
        self.height = bondInfo[1]*1.05
        self.fuelSurfaceNum = bondInfo[2]
        surfaceComment = "$Pin: Bond - 5% higher than fuel"
        cellComment = "$Pin: Bond"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.fuelSurfaceNum, self.surfaceNum, self.universe, cellComment)


class FuelClad(Unit):
    def makeComponent(self, cladInfo):
        self.radius = cladInfo[0]/2
        self.height = cladInfo[1]*1.05
        self.bondSurfaceNum = cladInfo[2]
        surfaceComment = "$Pin: Clad - 5% higher than fuel"
        cellComment = "$Pin: Clad"
        self.surfaceCard = getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.bondSurfaceNum, self.surfaceNum, self.universe, cellComment)

class FuelCoolant(Unit):
    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0]
        self.height = coolantInfo[1] * 1.05
        self.cladSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Coolant - 5% higher than fuel"
        cellComment = "$Pin: Wirewrap + Coolant"
        self.surfaceCard = getRHP(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getConcentricCell(self.cellNum, self.materialNum, self.material.density, self.cladSurfaceNum,
                                          self.surfaceNum, self.universe, cellComment)


class BlankCoolant(Unit):
    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0] / 2
        self.height = coolantInfo[1] * 1.05
        surfaceComment = "$Pin: Blank Pin - 5% higher than fuel"
        cellComment = "$Pin: Blank Pin Coolant"
        self.surfaceCard = getRHP(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density,
                                          self.surfaceNum, self.universe, cellComment)


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
        self.height = ductInfo[7] * 1.05
        self.makeComponent()

    def makeComponent(self):
        surfaceComment = "Assembly: Duct Inner Surface"
        cellComment = "Assembly: Inner Portion of Assembly"
        self.surfaceCard = getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getFuelLatticeCell(self.cellNum, self.surfaceNum, self.assemblyUniverse, self.latticeUniverse, cellComment)

class Duct(Unit):
    def makeComponent(self, ductInfo):
        self.flat2flat = ductInfo[0]
        self.height = ductInfo[1]
        surfaceComment = "$Assembly:Duct Outer Surface"
        cellComment = "$Assembly: Assembly Duct"
        self.surfaceCard = getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = getSingleCell(self.cellNum, self.materialNum, self.material.density,
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


def getRCC(radius, height, position, surfaceNum, comment):
    surfaceCard = "{} RCC {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], position[2], height, radius, comment)
    assert len(surfaceCard) < 80
    return surfaceCard
def getRHP(pitch, height, position, surfaceNum, comment):
    surfaceCard = "{} RHP {} {} {} 0 0 {} {} 0 0 {}".format(surfaceNum, position[0], position[1], position[2], height, pitch, comment)
    assert len(surfaceCard) < 80
    return surfaceCard

def getSingleCell(cellNum, matNum, density, surfaceNum, universe, comment):
    cellCard = "{} {} {} -{} u={} imp:n=1  {}".format(cellNum, matNum, density, surfaceNum, universe, comment)
    assert len(cellCard) < 80
    return cellCard

def getConcentricCell(cellNum, matNum, density, innerSurface, outerSurface, universe, comment):
    cellCard = "{} {} {} {} -{} u={} imp:n=1  {}".format(cellNum, matNum, density, innerSurface, outerSurface, universe, comment)
    assert len(cellCard) < 80
    return cellCard

def getFuelLatticeCell(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment):
    cellCard = "{} 0 -{} u={} fill={} imp:n=1 {}".format(cellNum, surfaceNum, assemblyUniverse, latticeUniverse, comment)
    assert len(cellCard) < 80
    return cellCard

def getAssemblyUniverseCell(cellNum, surfaceNum, universe, comment):
    cellCard = "{} 0 -{} fill={} imp:n=0 {}".format(cellNum, surfaceNum, universe, comment)
    assert len(cellCard) < 80
    return cellCard

def getMaterialCard(material, xc, matNum):
    materialCard = "c Material: {}; Density: {} atoms/bn*cm \nm{}".format(material.name, material.density, matNum)
    for isotope, atomDensity in material.atomPercent.items():
        materialCard += "      {}.{} {}\n".format(isotope, xc, atomDensity)
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

def getSmearAtomPercent():
    pass

# file_name = 'A271_Assembly'
#
# global_vars = gb.global_variables(file_name)
#
# assembly = FuelAssembly(['A271', '01A01', global_vars])
# fuelPin = assembly.fuel
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.bond
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.clad
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.coolant
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.blankCoolant
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.fuelUniverse
# print(fuelPin.cellCard)
#
# fuelPin = assembly.plenum
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.upperReflector
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)
#
# fuelPin = assembly.lowerReflector
# print(fuelPin.surfaceCard)
# print(fuelPin.cellCard)