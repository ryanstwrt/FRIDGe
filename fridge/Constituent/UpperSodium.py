from FRIDGe.fridge.Constituent import Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class UpperSodium(Constituent.Constituent):
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
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum,
                                             self.universe, cellComment)
