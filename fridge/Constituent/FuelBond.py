import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelBond(Constituent.Constituent):
    """Creates the bond material between the fuel and the inner cladding.
    The bond material is set to a default of 1% higher than the fuel."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.radius = 0
        self.height = 0
        self.fuelSurfaceNum = 0
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, bond_info):
        self.radius = bond_info[0] / 2
        self.height = bond_info[1]
        self.fuelSurfaceNum = bond_info[2]
        surface_comment = "$Pin: Bond - 1% higher than fuel"
        cell_comment = "$Pin: Bond"
        self.surfaceCard = mcnpCF.build_right_circular_cylinder_surface(self.radius, self.height, self.position,
                                                                        self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.build_concentric_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                     self.fuelSurfaceNum, self.surfaceNum, self.universe, cell_comment)
