import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class EveryThingElse(Constituent.Constituent):
    """"Creates the 'void', which MCNP requires a basic knowledge of."""
    def __init__(self, unit_info):
        self.cellNum = unit_info[0]
        self.assemblySurfaceNum = unit_info[1]
        self.make_component()

    def make_component(self):
        cell_comment = "$Everything Else"
        self.cellCard = mcnpCF.getEverythingElseCard(self.cellNum, self.assemblySurfaceNum, cell_comment)
