import fridge.Assembly.Assembly as Assembly
import fridge.Constituent.Smear as Smeared
import fridge.Constituent.LowerCoolant as Lowercoolant
import fridge.Constituent.OuterShell as Outershell
import fridge.Constituent.UpperCoolant as Uppercoolant
import fridge.Constituent.EveryThingElse as Everythingelse
import fridge.utilities.mcnpCreatorFunctions as mcnpCF
import yaml

import fridge.utilities.utilities


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
        self.lowerCoolant = None
        self.upperCoolant = None
        self.blankMaterial = None
        self.innerDuct = None
        self.duct = None
        self.assemblyShell = None
        self.everythingElse = None
        self.position = []
        self.assemblyCellList = []
        self.assemblySurfaceList = []
        self.assemblyMaterialList = []

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
        bottomCoolantPosition = fridge.utilities.utilities.getPosition(self.assemblyPosition, self.assemblyPitch,
                                                                       self.zPosition - excessCoolantHeight)
        bottomBlankPosition = fridge.utilities.utilities.getPosition(self.assemblyPosition, self.assemblyPitch, self.zPosition)
        upperBlankAssemblyPosition = fridge.utilities.utilities.getPosition(self.assemblyPosition, self.assemblyPitch,
                                                                            self.blankRegionHeight + self.zPosition)

        self.blankRegion = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                           self.blankMaterial, self.xcSet, bottomBlankPosition, self.materialNum],
                                          [self.ductOuterFlatToFlatMCNPEdge, self.blankRegionHeight], 'Blank Region'],
                                         voidMaterial=self.coolantMaterial, voidPercent=self.voidPercent)

        self.updateIdentifiers(False)
        self.lowerCoolant = Lowercoolant.LowerCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                       self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                       self.materialNum],
                                                      [excessCoolantHeight, self.ductOuterFlatToFlatMCNPEdge]],
                                                      voidPercent=self.voidPercent)

        self.updateIdentifiers(False)
        self.upperCoolant = Uppercoolant.UpperCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                       self.coolantMaterial, self.xcSet, upperBlankAssemblyPosition,
                                                       self.materialNum],
                                                      [excessCoolantHeight, self.ductOuterFlatToFlatMCNPEdge]],
                                                      voidPercent=self.voidPercent)

        self.updateIdentifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottomCoolantPosition,
                                                     self.materialNum],
                                                    [self.assemblyHeight, self.ductOuterFlatToFlat]])

        self.assemblyCellList = [self.blankRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]
        self.assemblySurfaceList = [self.blankRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]
        self.assemblyMaterialList = [self.blankRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]

        if 'Single' in self.globalVars.input_type:
            self.updateIdentifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])
            self.assemblyCellList.append(self.everythingElse)
