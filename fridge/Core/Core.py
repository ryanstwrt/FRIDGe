import fridge.Constituent.CoreCoolant as Corecoolant
import fridge.Constituent.ReactorVessel as Reactorvessel
import fridge.Constituent.EveryThingElse as Everytyhingelse
import fridge.utilities.utilities as utilities
import glob
import os

cur_dir = os.path.dirname(__file__)
core_directory = os.path.join(cur_dir, "../data/core")


class Core:
    """"Core class will hold all of the assemblies present in the core."""

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

    def read_core_data(self, core_file):
        """Assigns the variables used for the core."""
        core_yaml_file = glob.glob(os.path.join(core_directory, core_file + '.yaml'))
        inputs = utilities.yaml_reader(core_yaml_file, core_directory, core_file)
        self.name = inputs['Name']
        self.vesselThickness = inputs['Vessel Thickness']
        self.vesselMaterialString = inputs['Vessel Material']
        self.coolantMaterial = inputs['Coolant Material']
        return inputs

    def build_core(self, global_vars):
        """Builds all component required for a core."""
        last_assembly = self.assemblyList[-1]
        rings = int(last_assembly.assemblyPosition[:2])
        assembly = self.assemblyList[0]
        pitch = assembly.assemblyPitch
        self.coolantRadius = rings * pitch - pitch * 0.45
        self.coolantHeight = assembly.assemblyHeight * 1.1
        self.coolantPosition = assembly.assemblyShell.position
        self.coolantPosition[2] -= 10
        assembly_surface_list = []
        for assembly in self.assemblyList:
            assembly_surface_list.append(assembly.assemblyShell.surfaceNum)
        self.coreCoolant = Corecoolant.CoreCoolant([[0, global_vars.cellNumber, global_vars.surfaceNumber,
                                                     self.coolantMaterial, global_vars.xc_set,
                                                     self.coolantPosition, global_vars.materialNumber],
                                                    [self.coolantRadius, self.coolantHeight, assembly_surface_list]],
                                                   void_percent=global_vars.void_per)
        global_vars.update_numbering()
        self.vesselRadius = self.coolantRadius + self.vesselThickness
        self.vesselPosition = self.coolantPosition
        self.vesselPosition[2] -= self.vesselThickness
        self.vesselHeight = 2 * self.vesselThickness + self.coolantHeight
        self.reactorVessel = Reactorvessel.ReactorVessel([[0, global_vars.cellNumber, global_vars.surfaceNumber,
                                                         self.vesselMaterialString, global_vars.xc_set,
                                                         self.vesselPosition, global_vars.materialNumber],
                                                         [self.vesselRadius, self.vesselHeight,
                                                         self.coreCoolant.surfaceNum]])
        global_vars.update_numbering()
        self.everythingElse = Everytyhingelse.EveryThingElse([global_vars.cellNumber, self.reactorVessel.surfaceNum])

        self.coreCellList = [self.coreCoolant, self.reactorVessel, self.everythingElse]
        self.coreSurfaceList = [self.coreCoolant, self.reactorVessel]
        self.coreMaterialList = [self.coreCoolant, self.reactorVessel]
