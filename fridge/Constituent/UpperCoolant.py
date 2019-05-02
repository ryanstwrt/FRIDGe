import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class UpperCoolant(Constituent.Constituent):
    """Creates a region of sodium to compensate for any excess height specified in the assembly file.
    This is in addition to the lower coolant region. The sum of the upper and lower coolant region is the
    excess height from the assembly file."""
    def __init__(self, unit_info, void_percent=1.0):
        super().__init__(unit_info, void_percent=void_percent)
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, upper_coolant_info):
        excess_coolant_height = upper_coolant_info[0]
        flat_to_flat_universe = upper_coolant_info[1]
        surface_comment = "$Assembly: Upper Coolant"
        cell_comment = "$Assembly: Upper Coolant"
        self.surfaceCard = mcnpCF.getRHPRotated(flat_to_flat_universe, excess_coolant_height, self.position,
                                                self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cell_comment)
