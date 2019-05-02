import fridge.Constituent.Smear as Smear
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelCoolant(Smear.Smear):
    """Creates the coolant surrounding the fuel pin.
    This coolant is a homogenized material consisting of the coolant material and the wirewrap."""
    def __init__(self, unit_info, void_material='', void_percent=1.0):
        super().__init__(unit_info, void_material=void_material, void_percent=void_percent)
        self.cladSurfaceNum = 0

    def make_component(self, coolant_info):
        self.flat2flat = coolant_info[0]
        self.height = coolant_info[1]
        self.cladSurfaceNum = coolant_info[2]
        surface_comment = "$Pin: Coolant - 1% higher than fuel"
        cell_comment = "$Pin: Wirewrap + Coolant"
        self.surfaceCard = mcnpCF.build_right_hexagonal_prism_surface(self.flat2flat, self.height, self.position,
                                                                      self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.build_outside_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                  self.cladSurfaceNum, self.universe, cell_comment)
