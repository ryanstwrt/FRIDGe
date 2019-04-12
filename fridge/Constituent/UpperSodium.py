import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class UpperSodium(Constituent.Constituent):
    """Creates a region of sodium to compensate for any excess height specified in the assembly file.
    This is in addition to the lower sodium region. The sum of the upper and lower sodium region is the
    excess height from the assembly file."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, upperSodiumInfo):
        outerShell = upperSodiumInfo[0]
        flatToFlatUniverse = upperSodiumInfo[1]
        surfaceComment = "$Assembly: Upper Sodium"
        cellComment = "$Assembly: Upper Sodium"
        self.surfaceCard = mcnpCF.getRHP(flatToFlatUniverse, outerShell.excessNaHeight,
                                         outerShell.positionTopUpperReflector,  self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cellComment)
