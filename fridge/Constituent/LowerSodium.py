from FRIDGe.fridge.Constituent import Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class LowerSodium(Constituent.Constituent):
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, lowerSodiumInfo):
        outerShell = lowerSodiumInfo[0]
        flatToFlatUniverse = lowerSodiumInfo[1]
        surfaceComment = "$Assembly: Lower Sodium"
        cellComment = "$Assembly: Lower Sodium"
        self.surfaceCard = mcnpCF.getRHP(flatToFlatUniverse, outerShell.excessNaHeight,
                                         outerShell.positionBottomAssembly, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.density, self.surfaceNum,
                                             self.universe, cellComment)
