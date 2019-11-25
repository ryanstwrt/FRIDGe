import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF
import fridge.utilities.utilities as utilities


class FuelPin(Constituent.Constituent):
    """Creates a cylindrical fuel pin."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.radius = 0
        self.height = 0
        self.volume = 0
        self.pinsPerAssembly = 0
        self.fuel_position = self.position
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, pin_info):
        self.radius = pin_info[0] / 2
        self.height = pin_info[1]
        self.pinsPerAssembly = pin_info[2]
        self.volume = utilities.get_cylinder_volume(self.radius, self.height) * self.pinsPerAssembly
        surface_comment = "$Pin: Fuel"
        cell_comment = "$Pin: Fuel"
        self.surfaceCard = mcnpCF.build_right_circular_cylinder_surface(self.radius, self.height, self.position,
                                                                        self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.build_single_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.surfaceNum, self.universe, cell_comment, volume=self.volume)
