import FRIDGe.fridge.Assembly.Assembly as Assembly
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


class FuelAssembly(Assembly.Assembly):
    """
    Subclass of base assembly for fuel assemblies.

    Fuel assembly consists of upper/lower sodium region, upper/lower reflector regions,
    a plenum region, and a fuel region. All information for fuel, reflector and plenum regions are read in from the
    assembly yaml file.
    """

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
        self.bondAboveFuel = 0.0
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
        """ Reads in data from assembly yaml file."""
        with open(assemblyYamlFile[0], "r") as mat_file:
            inputs = yaml.safe_load(mat_file)
            self.getAssemblyInfo(inputs)
            self.getFuelRegionInfo(inputs)
            self.getPlenumRegionInfo(inputs)
            self.getReflectorInfo(inputs)

    def getAssembly(self):
        """Creates each component of the assembly."""
        self.fuelHeightWithBond = self.fuelHeight + self.bondAboveFuel
        definedHeight = 2 * self.reflectorHeight + self.fuelHeightWithBond + self.plenumHeight
        excessCoolantHeight = (self.assemblyHeight - definedHeight) / 2
        heightToUpperCoolant = definedHeight - self.reflectorHeight
        heightToUpperReflector = self.fuelHeightWithBond + self.plenumHeight
        upperCoolantPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, heightToUpperCoolant)
        upperReflectorPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, heightToUpperReflector)
        lowerReflectorPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, -self.reflectorHeight)
        bottomCoolantPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch,
                                                   -(self.reflectorHeight + excessCoolantHeight))

        self.assemblyUniverse = self.universe
        self.universe += 1
        self.pinUniverse = self.universe
        self.fuel = Fuelpin.FuelPin([[self.universe, self.cellNum, self.surfaceNum, self.fuelMaterial, self.xcSet,
                                      self.position, self.materialNum], [self.fuelDiameter, self.fuelHeight]])

        self.updateIdentifiers(False)
        self.bond = Fuelbond.FuelBond([[self.universe, self.cellNum, self.surfaceNum, self.bondMaterial, self.xcSet,
                                        self.position, self.materialNum],
                                       [self.cladID, self.fuelHeightWithBond, self.fuel.surfaceNum]])

        self.updateIdentifiers(False)
        self.clad = Fuelclad.FuelClad([[self.universe, self.cellNum, self.surfaceNum, self.cladMaterial, self.xcSet,
                                        self.position, self.materialNum],
                                       [self.cladOD, self.fuelHeightWithBond, self.bond.surfaceNum]])

        self.updateIdentifiers(False)
        smearedCoolantInfo = [self.fuelHeightWithBond, self.cladOD, self.wireWrapDiameter,
                              self.wireWrapAxialPitch, self.fuelPitch, self.coolantMaterial, self.cladMaterial]
        smearedCoolantMaterial = mcnpCF.getCoolantWireWrapSmear(smearedCoolantInfo)
        self.coolant = Fuelcoolant.FuelCoolant([[self.universe, self.cellNum, self.surfaceNum, smearedCoolantMaterial,
                                                 self.xcSet, self.position, self.materialNum],
                                                [self.fuelPitch, self.fuelHeightWithBond, self.clad.surfaceNum],
                                                'Wire Wrap + Coolant'])

        self.updateIdentifiers(True)
        self.blankUniverse = self.universe
        self.blankCoolant = Blankcoolant.BlankCoolant([[self.universe, self.cellNum, self.surfaceNum,
                                                        self.coolantMaterial, self.xcSet, self.position,
                                                        self.materialNum],
                                                       [self.fuelPitch, self.fuelHeightWithBond,
                                                        self.coolant.surfaceNum]])
        self.updateIdentifiers(True)
        self.latticeUniverse = self.universe
        self.fuelUniverse = Fueluniverse.FuelUniverse([self.pinUniverse, self.blankUniverse, self.pinsPerAssembly,
                                                       self.cellNum, self.blankCoolant.cellNum, self.latticeUniverse])

        self.updateIdentifiers(True)
        self.innerDuct = Innerduct.InnerDuct([[self.universe, self.cellNum, self.surfaceNum, '', self.xcSet,
                                               self.position, self.materialNum],
                                              [self.assemblyUniverse, self.latticeUniverse, self.ductInnerFlatToFlat,
                                               self.fuelHeightWithBond]])

        self.updateIdentifiers(False)
        self.plenum = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.plenumMaterial,
                                      self.xcSet, self.plenumPosition, self.materialNum],
                                     [self.ductInnerFlatToFlat, self.plenumHeight], 'Plenum'])

        self.updateIdentifiers(False)
        self.upperReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, self.xcSet, upperReflectorPosition,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'Upper Reflector'])

        self.updateIdentifiers(False)
        self.lowerReflector = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                              self.reflectorMaterial, self.xcSet, lowerReflectorPosition,
                                              self.materialNum],
                                             [self.ductInnerFlatToFlat, self.reflectorHeight], 'Lower Reflector'])

        self.updateIdentifiers(False)
        innerSurfaceNums = [self.innerDuct.surfaceNum, self.lowerReflector.surfaceNum, self. upperReflector.surfaceNum,
                            self.plenum.surfaceNum]
        self.duct = Outerduct.Duct([[self.assemblyUniverse, self.cellNum, self.surfaceNum, self.assemblyMaterial,
                                     self.xcSet, lowerReflectorPosition, self.materialNum],
                                    [self.ductOuterFlatToFlatMCNPEdge, definedHeight, innerSurfaceNums]])

        self.updateIdentifiers(False)
        self.lowerSodium = Lowersodium.LowerSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                     self.materialNum],
                                                    [excessCoolantHeight,
                                                     self.ductOuterFlatToFlatMCNPEdge]])

        self.updateIdentifiers(False)
        self.upperSodium = Uppersodium.UpperSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, upperCoolantPosition,
                                                     self.materialNum],
                                                    [excessCoolantHeight,
                                                     self.ductOuterFlatToFlatMCNPEdge]])

        self.updateIdentifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                     self.materialNum],
                                                    [self.assemblyHeight,  self.ductOuterFlatToFlat]])

        if 'Single' in self.globalVars.input_type:
            self.updateIdentifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])

    def getFuelRegionInfo(self, inputs):
        """Reads in the fuel region data from the assembly yaml file."""
        self.position = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, 0.0)
        self.cladOD = float(inputs['Pin Diameter'])
        self.cladID = self.cladOD - 2*float(inputs['Clad Thickness'])
        try:
            self.fuelDiameter = float(inputs["Fuel Diameter"])
        except KeyError:
            self.fuelDiameter = math.sqrt(float(inputs['Fuel Smear'])) * self.cladID
        self.fuelPitch = float(inputs['Pitch'])
        self.wireWrapDiameter = float(inputs['Wire Wrap Diameter'])
        self.wireWrapAxialPitch = float(inputs['Wire Wrap Axial Pitch'])
        self.fuelHeight = float(inputs['Fuel Height'])
        self.fuelMaterial = inputs['Fuel']
        self.cladMaterial = inputs['Clad']
        self.bondMaterial = inputs['Bond']
        self.bondAboveFuel = float(inputs["Bond Above Fuel"]) \
            if 'Bond Above Fuel' in inputs else 0.0

    def getPlenumRegionInfo(self, inputs):
        """Reads in the plenum region data from the assembly yaml file."""
        self.plenumHeight = float(inputs['Plenum Height'])
        self.plenumPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch,
                                                 self.fuelHeight + self.bondAboveFuel)
        self.plenumMaterial = inputs['Plenum Smear']

    def getReflectorInfo(self, inputs):
        """Reads in the reflector region data form the assembly yaml file."""
        self.reflectorHeight = float(inputs['Reflector Height'])
        self.reflectorMaterial = inputs['Reflector Smear']

