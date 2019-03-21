from FRIDGe.fridge.Constituent import Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelClad(Constituent.Constituent):
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.radius = 0
        self.height = 0
        self.bondSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, cladInfo):
        self.radius = cladInfo[0]/2
        self.height = cladInfo[1]*1.01
        self.bondSurfaceNum = cladInfo[2]
        surfaceComment = "$Pin: Clad - 1% higher than fuel"
        cellComment = "$Pin: Clad"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.density,
                                                 self.bondSurfaceNum, self.surfaceNum, self.universe, cellComment)
