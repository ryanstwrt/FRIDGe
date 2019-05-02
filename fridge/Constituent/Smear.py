import fridge.Constituent.Constituent as Constituent
import fridge.Material.Material
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Smear(Constituent.Constituent):
    """Creates a constituent which is a smear of materials."""
    def __init__(self, unit_info, void_material='', void_percent=1.0):
        self.universe = unit_info[0][0]
        self.cellNum = unit_info[0][1]
        self.surfaceNum = unit_info[0][2]
        self.materialXCLibrary = unit_info[0][4]
        self.material = unit_info[0][3]
        self.position = unit_info[0][5]
        self.materialNum = unit_info[0][6]
        self.componentName = unit_info[2]
        if void_percent == 1.0:
            self.material = fridge.Material.Material.get_smeared_material(self.material)
        else:
            self.material = fridge.Material.Material.get_smeared_material(self.material,
                                                                          void_material=void_material,
                                                                          void_percent=void_percent)
        self.make_component(unit_info[1])
        self.get_material_card(self.material)
        self.flat2flat = unit_info[1][0]
        self.height = unit_info[1][1]

    def make_component(self, unit_info):
        self.flat2flat = unit_info[0]
        self.height = unit_info[1]
        surface_comment = "$Assembly: {}".format(self.componentName)
        cell_comment = "$Assembly: {}".format(self.componentName)
        self.surfaceCard = mcnpCF.build_rotated_right_hexagonal_prism_surface(self.flat2flat, self.height,
                                                                              self.position, self.surfaceNum,
                                                                              surface_comment)
        self.cellCard = mcnpCF.build_single_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.surfaceNum, self.universe, cell_comment)

    def get_material_card(self, material_name):
        self.materialCard = mcnpCF.build_material_card(self.material, self.materialXCLibrary, self.materialNum)
