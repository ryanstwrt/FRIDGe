import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelClad(Constituent.Constituent):
    """Creates the jacket surrounding the fuel and bond material."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.radius = 0
        self.height = 0
        self.bondSurfaceNum = 0
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, clad_info):
        self.radius = clad_info[0] / 2
        self.height = clad_info[1]
        self.bondSurfaceNum = clad_info[2]
        surface_comment = "$Pin: Clad - 1% higher than fuel"
        cell_comment = "$Pin: Clad"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.bondSurfaceNum, self.surfaceNum, self.universe, cell_comment)
