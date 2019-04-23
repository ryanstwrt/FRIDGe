import fridge.utilities.mcnpCreatorFunctions as MCF
import fridge.utilities.materialReader as materialReader
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
        self.excessCoolant = None
        self.vessel = None
        self.vesselThickness = 0
        self.coolantSurfaceCard = ''
        self.coolantCellCard = ''
        self.materialCard = ''

    def getCoreData(self, coreFile):
        coreYamlFile = glob.glob(os.path.join(geo_dir, coreFile + '.yaml'))
        with open(coreYamlFile[0], 'r') as coreFile:
            inputs = yaml.safe_load(coreFile)
            self.name = inputs['Name']
            self.vesselThickness = inputs['Vessel Thickness']
        return inputs

    def buildExcessCoolant(self, global_vars):
        rings = (len(self.assemblyList) - 1) / 6 + 1
        assembly = self.assemblyList[0]
        pitch = assembly.assemblyPitch
        self.coolantRadius = rings * pitch - pitch / 2
        self.coolantHeight = assembly.assemblyHeight * 1.1
        self.position = assembly.assemblyShell.position
        self.position[2] -= 10
        self.coolantSurfaceCard = MCF.getRCC(self.coolantRadius, self.coolantHeight, self.position,
                                             global_vars.surfaceNumber, '$Coolant Surrounding Assemblies')
        assemblySurfaceList = []
        for assembly in self.assemblyList:
            assemblySurfaceList.append(assembly.assemblyShell.surfaceNum)
        print(assemblySurfaceList)
        self.material = materialReader.Material()
        self.material.setMaterial(assembly.coolantMaterial)
        self.materialCard = MCF.getMaterialCard(self.material, global_vars.xc_library, global_vars.materialNumber)
        self.coolantCellCard = MCF.getConcentricCellCoolant(global_vars.cellNumber, global_vars.materialNumber,
                                                    self.material.density, assemblySurfaceList,
                                                    global_vars.surfaceNumber, '$Coolant Surrounding Assemblies')

    def buildReactorVessel(self):
        pass