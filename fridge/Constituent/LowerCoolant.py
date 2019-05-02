import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF
import copy


class LowerCoolant(Constituent.Constituent):
    """Creates a region of sodium to compensate for any excess height specified in the assembly file.
    This is in addition to the upper coolant region. The sum of the upper and lower coolant region is the
    excess height from the assembly file."""
    def __init__(self, unit_info, void_percent=1.0):
        super().__init__(unit_info, void_percent=void_percent)
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, lower_coolant_info):
        excess_coolant_height = lower_coolant_info[0]
        flat_to_flat = lower_coolant_info[1]
        surface_comment = "$Assembly: Lower Coolant"
        cell_comment = "$Assembly: Lower Coolant"
        position = copy.deepcopy(self.position)
        position[2] -= 0.1
        lower_na_height = excess_coolant_height + 0.1
        self.surfaceCard = mcnpCF.getRHPRotated(flat_to_flat, lower_na_height, position, self.surfaceNum,
                                                surface_comment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cell_comment)
