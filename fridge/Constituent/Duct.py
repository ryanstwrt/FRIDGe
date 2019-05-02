import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Duct(Constituent.Constituent):
    """Encompasses the reflector, plenum, and fuel region in a hexagon duct."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.flat2flat = 0
        self.height = 0
        self.innerSurfaceNum = 0
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, duct_info):
        self.flat2flat = duct_info[0]
        self.height = duct_info[1]
        self.innerSurfaceNum = duct_info[2]
        surface_comment = "$Assembly: Duct Outer Surface"
        cell_comment = "$Assembly: Assembly Duct"
        self.surfaceCard = mcnpCF.getRHPRotated(self.flat2flat, self.height, self.position, self.surfaceNum,
                                                surface_comment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.innerSurfaceNum, self.surfaceNum, self.universe, cell_comment)
