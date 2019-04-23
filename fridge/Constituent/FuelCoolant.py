import fridge.Constituent.Smear as Smear
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelCoolant(Smear.Smear):
    """Creates the coolant surrounding the fuel pin.
    This coolant is a homogenized material consisting of the coolant material and the wirewrap."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.cladSurfaceNum = 0

    def makeComponent(self, coolantInfo):
        self.flat2flat = coolantInfo[0]
        self.height = coolantInfo[1]
        self.cladSurfaceNum = coolantInfo[2]
        surfaceComment = "$Pin: Coolant - 1% higher than fuel"
        cellComment = "$Pin: Wirewrap + Coolant"
        self.surfaceCard = mcnpCF.getRHP(self.flat2flat, self.height, self.position, self.surfaceNum,
                                                surfaceComment)
        self.cellCard = mcnpCF.getOutsideCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                              self.cladSurfaceNum, self.universe, cellComment)
