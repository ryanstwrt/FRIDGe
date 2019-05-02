import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class BlankCoolant(Constituent.Constituent):
    """Creates a hexagon pin of coolant material for use around the fuel lattice."""
    def __init__(self, unit_info, void_percent=1.0):
        super().__init__(unit_info, void_percent=void_percent)
        self.pitch = 0
        self.height = 0
        self.blankCoolantSurfaceNum = 0
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, coolant_info):
        self.pitch = coolant_info[0] / 2
        self.height = coolant_info[1]
        self.blankCoolantSurfaceNum = coolant_info[2]
        surface_comment = "$Pin: Blank Pin - 1% higher than fuel"
        cell_comment = "$Pin: Blank Pin Coolant"
        self.surfaceCard = mcnpCF.build_right_hexagonal_prism_surface(self.pitch, self.height, self.position,
                                                                      self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.build_single_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.blankCoolantSurfaceNum, self.universe, cell_comment)
