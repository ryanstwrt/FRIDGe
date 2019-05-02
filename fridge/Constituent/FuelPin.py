import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelPin(Constituent.Constituent):
    """Creates a template for the assembly fuel pin."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.radius = 0
        self.height = 0
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, pin_info):
        self.radius = pin_info[0] / 2
        self.height = pin_info[1]
        surface_comment = "$Pin: Fuel"
        cell_comment = "$Pin: Fuel"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cell_comment)
