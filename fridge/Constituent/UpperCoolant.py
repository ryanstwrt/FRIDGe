import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class UpperSodium(Constituent.Constituent):
    """Creates a region of sodium to compensate for any excess height specified in the assembly file.
    This is in addition to the lower coolant region. The sum of the upper and lower coolant region is the
    excess height from the assembly file."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, upperCoolantInfo):
        excessCoolantHeight = upperCoolantInfo[0]
        flatToFlatUniverse = upperCoolantInfo[1]
        surfaceComment = "$Assembly: Upper Coolant"
        cellComment = "$Assembly: Upper Coolant"
        self.surfaceCard = mcnpCF.getRHP(flatToFlatUniverse, excessCoolantHeight, self.position,  self.surfaceNum,
                                         surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cellComment)
