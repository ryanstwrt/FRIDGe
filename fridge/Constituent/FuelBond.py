import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelBond(Constituent.Constituent):
    """Creates the bond material between the fuel and the inner cladding.
    The bond material is set to a default of 1% higher than the fuel."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.radius = 0
        self.height = 0
        self.fuelSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, bondInfo):
        self.radius = bondInfo[0]/2
        self.height = bondInfo[1]
        self.fuelSurfaceNum = bondInfo[2]
        surfaceComment = "$Pin: Bond - 1% higher than fuel"
        cellComment = "$Pin: Bond"
        self.surfaceCard = mcnpCF.getRCC(self.radius, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.fuelSurfaceNum, self.surfaceNum, self.universe, cellComment)
