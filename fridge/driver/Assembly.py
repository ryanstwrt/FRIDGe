import FRIDGe.fridge.Constituent.FuelPin as Fuelpin
import FRIDGe.fridge.Constituent.FuelBond as Fuelbond
import FRIDGe.fridge.Constituent.FuelClad as Fuelclad
import FRIDGe.fridge.Constituent.FuelCoolant as Fuelcoolant
import FRIDGe.fridge.Constituent.BlankCoolant as Blankcoolant
import FRIDGe.fridge.Constituent.FuelUniverse as Fueluniverse
import FRIDGe.fridge.Constituent.InnerDuct as Innerduct
import FRIDGe.fridge.Constituent.Duct as Outerduct
import FRIDGe.fridge.Constituent.Smear as Smeared
import FRIDGe.fridge.Constituent.OuterShell as Outershell
import FRIDGe.fridge.Constituent.UpperSodium as Uppersodium
import FRIDGe.fridge.Constituent.LowerSodium as Lowersodium
import FRIDGe.fridge.Constituent.EveryThingElse as Everythingelse
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF
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
        self.universe += 1
        self.pinUniverse = self.universe
        self.fuel = Fuelpin.FuelPin([[self.universe, self.cellNum, self.surfaceNum, self.fuelMaterial, '82C',
                                      self.position, self.materialNum], [self.fuelDiameter, self.fuelHeight]])
        self.updateIdentifiers()
        self.bond = Fuelbond.FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, '82C',
                                        self.position, self.materialNum],
                                       [self.cladID, self.fuelHeight, self.fuel.surfaceNum]])
        self.updateIdentifiers()
        self.clad = Fuelclad.FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, '82C',
                                        self.position, self.materialNum],
                                       [self.cladOD, self.fuelHeight, self.bond.surfaceNum]])
        self.updateIdentifiers()
        self.coolant = Fuelcoolant.FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial,
                                                 '82C', self.position, self.materialNum],
                                                [self.fuelPitch, self.fuelHeight, self.clad.surfaceNum]])
        self.updateIdentifiers()
        self.universe += 1
        self.blankUniverse = self.universe
        self.blankCoolant = Blankcoolant.BlankCoolant([[self.universe, self.cellNum, self.surfaceNum,
                                                        self.coolantMaterial, '82C', self.position, self.materialNum],
                                                       [self.fuelPitch, self.fuelHeight, self.coolant.surfaceNum]])
        self.updateIdentifiers()
        self.universe += 1
        self.latticeUniverse = self.universe
        self.fuelUniverse = Fueluniverse.FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly,
                                                       self.cellNum, self.blankCoolant.cellNum, self.latticeUniverse])
        self.updateIdentifiers()
        self.innerDuct = Innerduct.InnerDuct([self.universe, self.cellNum, self.surfaceNum, self.assemblyUniverse,
                                              self.latticeUniverse, self.position, self.ductInnerFlatToFlat,
                                              self.fuelHeight])
        self.updateIdentifiers()
        self.duct = Outerduct.Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                     self.position, self.materialNum],
                                    [self.ductOuterFlatToFlatUniverse, self.fuelHeight, self.innerDuct.surfaceNum]])
        self.updateIdentifiers()
        self.plenum = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.plenumMaterial, '82C',
                                      self.plenumPosition, self.materialNum],
                                     [self.ductOuterFlatToFlatUniverse, self.plenumHeight], 'plenum'])
        self.updateIdentifiers()
        self.upperReflectorPosition = self.position
        self.upperReflectorPosition[2] += self.fuelHeight * 1.01 + self.plenumHeight
        self.upperReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, '82C', self.position, self.materialNum],
                                             [self.ductOuterFlatToFlatUniverse, self.reflectorHeight],
                                             'upper Reflector'])

        self.updateIdentifiers()
        self.lowerReflectorPosition = self.position
        self.lowerReflectorPosition[2] = -self.reflectorHeight
        self.lowerReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, '82C', self.position, self.materialNum],
                                             [self.ductOuterFlatToFlatUniverse, self.reflectorHeight],
                                             'lower Reflector'])
        self.updateIdentifiers()

        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', [], self.materialNum],
                                                    [self.reflectorHeight, self.fuelHeight, self.plenumHeight,
                                                     self.assemblyHeight, self.ductOuterFlatToFlat,
                                                     self.assemblyPosition]])

        self.updateIdentifiers()
        self.lowerSodium = Lowersodium.LowerSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', self.position, self.materialNum],
                                                    [self.assemblyShell, self.ductOuterFlatToFlatUniverse]])

        self.updateIdentifiers()
        self.upperSodium = Uppersodium.UpperSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', self.position, self.materialNum],
                                                    [self.assemblyShell, self.ductOuterFlatToFlatUniverse]])

        if 'Single' in self.globalVars.input_type:
            self.updateIdentifiers()
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])

    def getFuelRegionInfo(self, inputs):
        self.position = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, 0.0)
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
        self.plenumPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, self.fuelHeight * 1.01)
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
