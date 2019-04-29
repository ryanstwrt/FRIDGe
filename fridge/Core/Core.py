import fridge.Constituent.CoreCoolant as Corecoolant
import fridge.Constituent.ReactorVessel as Reactorvessel
import fridge.Constituent.EveryThingElse as Everytyhingelse
import glob
import yaml
import os

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/core")


class Core:
    """"core class will hold all of the assemblies present in the core."""

    def __init__(self):
        self.name = ''
        self.assemblyList = []
        self.vesselThickness = 0
        self.coolantSurfaceCard = ''
        self.coolantCellCard = ''
        self.materialCard = ''
        self.vesselMaterial = None
        self.vesselMaterialString = ''
        self.coolantRadius = 0
        self.coolantHeight = 0
        self.coolantPosition = []
        self.coolantMaterial = None
        self.vesselRadius = 0
        self.vesselHeight = 0
        self.vesselPosition = []
        self.vesselSurfaceCard = ''
        self.coreCellList = []
        self.coreSurfaceList = []
        self.coreMaterialList = []
        self.everythingElse = None
        self.coreCoolant = None
        self.reactorVessel = None

    def getCoreData(self, coreFile):
        coreYamlFile = glob.glob(os.path.join(geo_dir, coreFile + '.yaml'))
        with open(coreYamlFile[0], 'r') as coreFile:
            inputs = yaml.safe_load(coreFile)
            self.name = inputs['Name']
            self.vesselThickness = inputs['Vessel Thickness']
            self.vesselMaterialString = inputs['Vessel Material']
            self.coolantMaterial = inputs['Coolant Material']
        return inputs

    def getCore(self, global_vars):
        lastAssembly = self.assemblyList[-1]
        rings = int(lastAssembly.assemblyPosition[:2])
        assembly = self.assemblyList[0]
        pitch = assembly.assemblyPitch
        self.coolantRadius = rings * pitch - pitch * 0.45
        self.coolantHeight = assembly.assemblyHeight * 1.1
        self.coolantPosition = assembly.assemblyShell.position
        self.coolantPosition[2] -= 10
        assemblySurfaceList = []
        for assembly in self.assemblyList:
            assemblySurfaceList.append(assembly.assemblyShell.surfaceNum)
        self.coreCoolant = Corecoolant.CoreCoolant([[0, global_vars.cellNumber, global_vars.surfaceNumber,
                                                     self.coolantMaterial, global_vars.xc_set,
                                                     self.coolantPosition, global_vars.materialNumber],
                                                    [self.coolantRadius, self.coolantHeight, assemblySurfaceList]],
                                                   voidPercent=global_vars.void_per)
        global_vars.updateNumbering()
        self.vesselRadius = self.coolantRadius + self.vesselThickness
        self.vesselPosition = self.coolantPosition
        self.vesselPosition[2] -= self.vesselThickness
        self.vesselHeight = 2 * self.vesselThickness + self.coolantHeight
        self.reactorVessel = Reactorvessel.ReactorVessel([[0, global_vars.cellNumber, global_vars.surfaceNumber,
                                                         self.vesselMaterialString, global_vars.xc_set,
                                                         self.vesselPosition, global_vars.materialNumber],
                                                         [self.vesselRadius, self.vesselHeight,
                                                         self.coreCoolant.surfaceNum]])
        global_vars.updateNumbering()
        self.everythingElse = Everytyhingelse.EveryThingElse([global_vars.cellNumber, self.reactorVessel.surfaceNum])

        self.coreCellList = [self.coreCoolant, self.reactorVessel, self.everythingElse]
        self.coreSurfaceList = [self.coreCoolant, self.reactorVessel]
        self.coreMaterialList = [self.coreCoolant, self.reactorVessel]
