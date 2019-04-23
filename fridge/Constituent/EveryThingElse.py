import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class EveryThingElse(Constituent.Constituent):
    """"Creates the 'void', which MCNP requires a basic knowledge of."""
    def __init__(self, unitInfo):
        self.cellNum = unitInfo[0]
        self.assemblySurfaceNum = unitInfo[1]
        self.makeComponent()

    def makeComponent(self):
        cellComment = "$Everything Else"
        self.cellCard = mcnpCF.getEverythingElseCard(self.cellNum, self.assemblySurfaceNum, cellComment)
