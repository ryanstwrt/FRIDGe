from FRIDGe.fridge.Assembly import Assembly
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
import yaml
import math
import copy


class FuelAssembly(Assembly.Assembly):

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

        assemblyYamlFile = Assembly.getAssemblyLocation(self.assemblyDesignation)
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
        self.updateIdentifiers(False)
        self.bond = Fuelbond.FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, '82C',
                                        self.position, self.materialNum],
                                       [self.cladID, self.fuelHeight, self.fuel.surfaceNum]])
        self.updateIdentifiers(False)
        self.clad = Fuelclad.FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, '82C',
                                        self.position, self.materialNum],
                                       [self.cladOD, self.fuelHeight, self.bond.surfaceNum]])
        self.updateIdentifiers(False)
        self.coolant = Fuelcoolant.FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, self.coolantMaterial,
                                                 '82C', self.position, self.materialNum],
                                                [self.fuelPitch, self.fuelHeight, self.clad.surfaceNum]])
        self.updateIdentifiers(True)
        self.blankUniverse = self.universe
        self.blankCoolant = Blankcoolant.BlankCoolant([[self.universe, self.cellNum, self.surfaceNum,
                                                        self.coolantMaterial, '82C', self.position, self.materialNum],
                                                       [self.fuelPitch, self.fuelHeight, self.coolant.surfaceNum]])
        self.updateIdentifiers(True)
        self.latticeUniverse = self.universe
        self.fuelUniverse = Fueluniverse.FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly,
                                                       self.cellNum, self.blankCoolant.cellNum, self.latticeUniverse])
        self.updateIdentifiers(True)
        self.innerDuct = Innerduct.InnerDuct([[self.universe, self.cellNum, self.surfaceNum, '', '82c', self.position,
                                              self.materialNum], [self.assemblyUniverse, self.latticeUniverse,
                                              self.ductInnerFlatToFlat, self.fuelHeight]])
        self.updateIdentifiers(False)
        self.plenum = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.plenumMaterial, '82C',
                                      self.plenumPosition, self.materialNum],
                                     [self.ductInnerFlatToFlat, self.plenumHeight], 'plenum'])

        self.updateIdentifiers(False)
        self.upperReflectorPosition = copy.deepcopy(self.position)
        self.upperReflectorPosition[2] = self.fuelHeight * 1.01 + self.plenumHeight
        self.upperReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, '82C', self.upperReflectorPosition,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'upper Reflector'])
        self.updateIdentifiers(False)
        self.lowerReflectorPosition = self.position
        self.lowerReflectorPosition[2] = -self.reflectorHeight
        self.lowerReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, '82C', self.lowerReflectorPosition,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'lower Reflector'])
        self.updateIdentifiers(False)
        innerSurfaceNums = [self.innerDuct.surfaceNum, self.lowerReflector.surfaceNum, self. upperReflector.surfaceNum,
                            self.plenum.surfaceNum]
        reflector2ReflectorHeight = self.reflectorHeight * 2 + self.plenumHeight + self.fuelHeight * 1.01
        self.duct = Outerduct.Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.coolantMaterial, '82C',
                                     self.lowerReflectorPosition, self.materialNum],
                                    [self.ductOuterFlatToFlatMCNPEdge, reflector2ReflectorHeight, innerSurfaceNums]])
        self.updateIdentifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', [], self.materialNum],
                                                    [self.reflectorHeight, self.fuelHeight, self.plenumHeight,
                                                     self.assemblyHeight, self.ductOuterFlatToFlat,
                                                     self.assemblyPosition]])
        self.updateIdentifiers(False)
        self.lowerSodium = Lowersodium.LowerSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', self.position, self.materialNum],
                                                    [self.assemblyShell, self.ductOuterFlatToFlatMCNPEdge]])

        self.updateIdentifiers(False)
        self.upperSodium = Uppersodium.UpperSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, '82C', self.position, self.materialNum],
                                                    [self.assemblyShell, self.ductOuterFlatToFlatMCNPEdge]])

        if 'Single' in self.globalVars.input_type:
            self.updateIdentifiers(False)
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
