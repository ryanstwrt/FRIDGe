import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class InnerDuct(Constituent.Constituent):
    """Creates the inner surface for the duct surrounding the reflector, plenum and fuel regions."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.assemblyUniverse = 0
        self.latticeUniverse = 0
        self.flat2flat = 0
        self.height = 0
        self.make_component(unit_info[1])

    def make_component(self, duct_info):
        self.assemblyUniverse = duct_info[0]
        self.latticeUniverse = duct_info[1]
        self.flat2flat = duct_info[2]
        self.height = duct_info[3]
        surface_comment = "$Assembly: Duct Inner Surface"
        cell_comment = "$Assembly: Inner Portion of Assembly"
        self.surfaceCard = mcnpCF.getRHPRotated(self.flat2flat, self.height, self.position, self.surfaceNum,
                                                surface_comment)
        self.cellCard = mcnpCF.getFuelLatticeCell(self.cellNum, self.surfaceNum, self.assemblyUniverse,
                                                  self.latticeUniverse, cell_comment)
