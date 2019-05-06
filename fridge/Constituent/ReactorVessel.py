import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class ReactorVessel(Constituent.Constituent):
    """Creates a cylinder around the Core Coolant to make the reactor vessel."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.vesselRadius = unit_info[1][0]
        self.vesselHeight = unit_info[1][1]
        self.coreCoolantSurfaceNum = unit_info[1][2]
        self.get_material_card(unit_info[0][3])
        self.make_component([1])

    def make_component(self, unit_info):
        self.surfaceCard = mcnpCF.build_right_circular_cylinder_surface(self.vesselRadius, self.vesselHeight,
                                                                        self.position, self.surfaceNum,
                                                                        '$Vessel surrounding the core')
        self.cellCard = mcnpCF.build_concentric_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                     [self.coreCoolantSurfaceNum], self.surfaceNum, '',
                                                     '$Reactor Vessel')
