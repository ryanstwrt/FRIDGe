import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelBond(Constituent.Constituent):
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.radius = 0
        self.height = 0
        self.fuelSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, bondInfo):
        self.radius = bondInfo[0]/2
        self.height = bondInfo[1]*1.01
        self.fuelSurfaceNum = bondInfo[2]
        surfaceComment = "$Pin: Bond - 1% higher than fuel"
        cellComment = "$Pin: Bond"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.fuelSurfaceNum, self.surfaceNum, self.universe, cellComment)
