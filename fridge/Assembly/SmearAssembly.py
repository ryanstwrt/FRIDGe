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
    Subclass of base assembly for a smear assembly.

    Blank assemblies consist of a smear region and upper/lower sodium region. All information for assembly is read
    in from an assembly yaml file.
    """

    def __init__(self, assembly_information):
        super().__init__(assembly_information)
        self.assemblyUniverse = 0
        self.smearRegionHeight = 0
        self.smearRegion = None
        self.lowerCoolant = None
        self.upperCoolant = None
        self.smearMaterial = None
        self.innerDuct = None
        self.duct = None
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
        self.smearMaterial = self.inputs['Blank Smear']
        self.smearRegionHeight = self.inputs['Blank Height']

    def build_smear_assembly(self):
        """Build the cell, surface, and material cards for the smear assembly."""
        self.assemblyUniverse = self.universe
        excess_coolant_height = (self.assemblyHeight - self.smearRegionHeight) / 2
        bottom_coolant_position = fridge.utilities.utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                                          self.zPosition - excess_coolant_height)
        bottom_smear_position = fridge.utilities.utilities.get_position_for_hex_lattice(self.assemblyPosition, self.assemblyPitch,
                                                                                        self.zPosition)
        upper_smear_assembly_position = fridge.utilities.utilities.get_position_for_hex_lattice(self.assemblyPosition,
                                                                                                self.assemblyPitch,
                                                                                                self.smearRegionHeight + self.zPosition)

        self.smearRegion = Smeared.Smear([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                           self.smearMaterial, self.xcSet, bottom_smear_position, self.materialNum],
                                          [self.ductOuterFlatToFlatMCNPEdge, self.smearRegionHeight], 'Blank Region'],
                                         void_material=self.coolantMaterial, void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.lowerCoolant = Lowercoolant.LowerCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                       self.coolantMaterial, self.xcSet, bottom_coolant_position,
                                                       self.materialNum],
                                                      [excess_coolant_height, self.ductOuterFlatToFlatMCNPEdge]],
                                                      void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.upperCoolant = Uppercoolant.UpperCoolant([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                       self.coolantMaterial, self.xcSet, upper_smear_assembly_position,
                                                       self.materialNum],
                                                      [excess_coolant_height, self.ductOuterFlatToFlatMCNPEdge]],
                                                      void_percent=self.voidPercent)

        self.update_global_identifiers(False)
        self.assemblyShell = Outershell.OuterShell([[self.assemblyUniverse, self.cellNum, self.surfaceNum,
                                                     self.coolantMaterial, self.xcSet, bottom_coolant_position,
                                                     self.materialNum],
                                                    [self.assemblyHeight, self.ductOuterFlatToFlat]])

        self.assemblyCellList = [self.smearRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]
        self.assemblySurfaceList = [self.smearRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]
        self.assemblyMaterialList = [self.smearRegion, self.lowerCoolant, self.upperCoolant, self.assemblyShell]

        if 'Single' in self.globalVars.input_type:
            self.update_global_identifiers(False)
            self.everythingElse = Everythingelse.EveryThingElse([self.cellNum, self.assemblyShell.surfaceNum])
            self.assemblyCellList.append(self.everythingElse)
