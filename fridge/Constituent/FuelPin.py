import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelPin(Constituent.Constituent):
    """Creates a template for the assembly fuel pin."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.radius = 0
        self.height = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, pinInfo):
        self.radius = pinInfo[0]/2
        self.height = pinInfo[1]
        surfaceComment = "$Pin: Fuel"
        cellComment = "$Pin: Fuel"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cellComment)
