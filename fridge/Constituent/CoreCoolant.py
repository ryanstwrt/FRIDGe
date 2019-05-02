import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class CoreCoolant(Constituent.Constituent):
    def __init__(self, unit_info, void_percent=1.0):
        super().__init__(unit_info, void_percent=void_percent)
        self.coolantRadius = unit_info[1][0]
        self.coolantHeight = unit_info[1][1]
        self.assemblySurfaceList = unit_info[1][2]
        self.get_material_card(unit_info[0][3])
        self.make_component([1])

    def make_component(self, unit_info):
        self.surfaceCard = mcnpCF.build_right_circular_cylinder_surface(self.coolantRadius, self.coolantHeight,
                                                                        self.position, self.surfaceNum,
                                                                        '$Coolant Surrounding Assemblies')
        self.cellCard = mcnpCF.build_concentric_cell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                     self.assemblySurfaceList, self.surfaceNum, '',
                                                     '$Coolant Surrounding Assemblies')
