import FRIDGe.fridge.Assembly.Assembly as Assembly
import FRIDGe.fridge.Constituent.Smear as Smeared
import FRIDGe.fridge.Constituent.LowerSodium as Lowersodium
import FRIDGe.fridge.Constituent.OuterShell as Outershell
import FRIDGe.fridge.Constituent.UpperSodium as Uppersodium
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF
import yaml


class BlankAssembly(Assembly.Assembly):
    """
    Subclass of base assembly for a blank assembly.

    Blank assemblies consist of a blank region and upper/lower sodium region. All information for assembly is read
    in from an assembly yaml file.
    """

    def __init__(self, assemblyInformation):
        super().__init__(assemblyInformation)
        self.assemblyUniverse = 0
        self.blankRegionHeight = 0
        self.blankRegion = None
        self.lowerSodium = None
        self.upperSodium = None
        self.blankMaterial = None
        self.innerDuct = None
        self.duct = None
        self.assemblyShell = None
        self.position = []

        assemblyYamlFile = Assembly.getAssemblyLocation(self.assemblyDesignation)
        self.setAssembly(assemblyYamlFile)
        self.getAssembly()

    def setAssembly(self, assemblyYamlFile):
        with open(assemblyYamlFile[0], "r") as mat_file:
            inputs = yaml.safe_load(mat_file)
            self.getAssemblyInfo(inputs)
            self.blankMaterial = inputs['Blank Smear']
            self.blankRegionHeight = inputs['Blank Height']

    def getAssembly(self):
        self.assemblyUniverse = self.universe
        excessCoolantHeight = (self.assemblyHeight - self.blankRegionHeight) / 2
        bottomCoolantPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, self.zPosition -
                                                                                                excessCoolantHeight)
        bottomBlankPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch, self.zPosition)
        upperBlankAssemblyPosition = mcnpCF.getPosition(self.assemblyPosition, self.assemblyPitch,
                                                        self.blankRegionHeight + self.zPosition)

        self.blankRegion = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                           self.blankMaterial, self.xcSet, bottomBlankPosition, self.materialNum],
                                          [self.ductOuterFlatToFlatMCNPEdge, self.blankRegionHeight], 'Blank Region'])

        self.updateIdentifiers(False)
        self.lowerSodium = Lowersodium.LowerSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                     self.materialNum],
                                                    [excessCoolantHeight, self.ductOuterFlatToFlatMCNPEdge]])

        self.updateIdentifiers(False)
        self.upperSodium = Uppersodium.UpperSodium([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, upperBlankAssemblyPosition,
                                                     self.materialNum],
                                                    [excessCoolantHeight, self.ductOuterFlatToFlatMCNPEdge]])

        self.updateIdentifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                     self.materialNum],
                                                    [self.assemblyHeight, self.ductOuterFlatToFlat]])


