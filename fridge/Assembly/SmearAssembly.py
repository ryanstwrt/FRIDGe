import fridge.Assembly.Assembly as Assembly
import fridge.Constituent.Smear as Smeared
import fridge.Constituent.OuterShell as Outershell
import fridge.Constituent.EveryThingElse as Everythingelse
import fridge.utilities.utilities as utilities


class SmearAssembly(Assembly.Assembly):
    """
    Subclass of base assembly for a smear assembly.

    .82c assemblies consist of a smear region and upper/lower sodium region. All information for assembly is read
    in from an assembly yaml file.
    """

    def __init__(self, assembly_information):
        super().__init__(assembly_information)
        self.assemblyUniverse = 0
        self.smearRegionHeight = 0
        self.smearRegions = {}
        self.assemblyShell = None
        self.everythingElse = None
        self.position = []
        self.assemblyCellList = []
        self.assemblySurfaceList = []
        self.assemblyMaterialList = []

        self.get_smear_assembly_data()
        self.build_smear_assembly()

    def get_smear_assembly_data(self):
        """Assign assembly data for the smear assembly."""
        self.get_assembly_data(self.inputs)
        self.axialRegions = self.inputs['Axial Regions']
        self.axialRegionDict = {}
        for region in self.axialRegions:
            try:
                self.axialRegionDict[region] = self.inputs['Axial Region {}'.format(region)]
                self.smearRegionHeight += self.axialRegionDict[region]['Smear Height']
            except:
                print("Failed to create axial region {} for assembly {}, "
                      "ensure this region is defined".format(region, self.assembly_file_name))
                exit()
        # Update for perturbations
        if bool(self.globalVars.assembly_perturbations):
            self.update_perturbations()

    def build_smear_assembly(self):
        """Build the cell, surface, and material cards for the smear assembly."""
        self.assemblyUniverse = self.universe
        cur_position = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch, self.zPosition)
        cur_position[2] -= 0.1

        for region, region_dict in self.axialRegionDict.items():
            if region == 1:
                smear_height = region_dict['Smear Height'] + 0.1
            else:
                smear_height = region_dict['Smear Height']
            self.smearRegions[region] = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                        region_dict['Smear Materials'], self.xcSet,
                                                        cur_position, self.materialNum],
                                                       [self.ductOuterFlatToFlatMCNPEdge, smear_height],
                                                       region_dict['Smear Name']], void_material=self.coolantMaterial,
                                                      void_percent=self.voidPercent)
            if region == 1:
                cur_position[2] += region_dict['Smear Height'] + 0.1
            else:
                cur_position[2] += region_dict['Smear Height']
            self.update_global_identifiers(False)
            self.assemblyCellList.append(self.smearRegions[region])
            self.assemblySurfaceList.append(self.smearRegions[region])
            self.assemblyMaterialList.append(self.smearRegions[region])

        shell_pos = utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch, self.zPosition)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, shell_pos, self.materialNum],
                                                    [self.assemblyHeight, self.ductOuterFlatToFlat]])

        self.assemblyCellList.append(self.assemblyShell)
        self.assemblySurfaceList.append(self.assemblyShell)
        self.assemblyMaterialList.append(self.assemblyShell)

        if 'Single' in self.globalVars.input_type:
            self.update_global_identifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])
            self.assemblyCellList.append(self.everythingElse)
