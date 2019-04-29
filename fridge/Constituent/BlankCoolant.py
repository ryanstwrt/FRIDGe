import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class BlankCoolant(Constituent.Constituent):
    """Creates a hexagon pin of coolant material for use around the fuel lattice."""
    def __init__(self, unitInfo, voidPercent=1.0):
        super().__init__(unitInfo, voidPercent=voidPercent)
        self.pitch = 0
        self.height = 0
        self.blankCoolantSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, coolantInfo):
        self.pitch = coolantInfo[0] / 2
        self.height = coolantInfo[1]
        self.blankCoolantSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Blank Pin - 1% higher than fuel"
        cellComment = "$Pin: Blank Pin Coolant"
        self.surfaceCard = mcnpCF.getRHP(self.pitch, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                             self.blankCoolantSurfaceNum, self.universe, cellComment)
