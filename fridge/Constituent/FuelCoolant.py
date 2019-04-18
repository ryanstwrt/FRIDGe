import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelCoolant(Constituent.Constituent):
    """Creates the coolant surrounding the fuel pin.
    This coolant is a homogenized material consisting of the coolant material and the wirewrap."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.pitch = 0
        self.height = 0
        self.cladSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0]
        self.height = coolantInfo[1]
        self.cladSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Coolant - 1% higher than fuel"
        cellComment = "$Pin: Wirewrap + Coolant"
        self.surfaceCard = mcnpCF.getRHPRotated(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getOutsideCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                              self.cladSurfaceNum, self.universe, cellComment)
