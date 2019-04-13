import FRIDGe.fridge.Assembly.Assembly as Assembly
import FRIDGe.fridge.Constituent.Smear as Smeared
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
        self.blankPosition = []

        assemblyYamlFile = Assembly.getAssemblyLocation(self.assemblyDesignation)
        self.setAssembly(assemblyYamlFile)
        self.getAssembly()

    def setAssembly(self, assemblyYamlFile):
        with open(assemblyYamlFile[0], "r") as mat_file:
            inputs = yaml.safe_load(mat_file)
            self.getAssemblyInfo(inputs)

    def getAssembly(self):
        self.assemblyUniverse = self.universe
        self.universe += 1
        self.blankRegion = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                           self.blankMaterial, '82C', self.blankPosition,
                                           self.materialNum],
                                           [self.ductInnerFlatToFlat, self.blankRegionHeight], 'Blank Region'])