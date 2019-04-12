import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class EveryThingElse(Constituent.Constituent):
    """"Creates the 'void', which MCNP requires a basic knowledge of."""
    def __init__(self, unitInfo):
        self.cellNum = unitInfo[0]
        self.assemblySurfaceNum = unitInfo[1]
        self.makeComponent()

    def makeComponent(self):
        cellComment = "$Assembly: Outside Assembly"
        self.cellCard = mcnpCF.getEverythingElseCard(self.cellNum, self.assemblySurfaceNum, cellComment)
