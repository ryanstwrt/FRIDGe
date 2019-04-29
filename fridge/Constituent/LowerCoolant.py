import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF
import copy


class LowerCoolant(Constituent.Constituent):
    """Creates a region of sodium to compensate for any excess height specified in the assembly file.
    This is in addition to the upper coolant region. The sum of the upper and lower coolant region is the
    excess height from the assembly file."""
    def __init__(self, unitInfo, voidPercent=1.0):
        super().__init__(unitInfo, voidPercent=voidPercent)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, lowerCoolantInfo):
        excessCoolantHeight = lowerCoolantInfo[0]
        flatToFlat = lowerCoolantInfo[1]
        surfaceComment = "$Assembly: Lower Coolant"
        cellComment = "$Assembly: Lower Coolant"
        position = copy.deepcopy(self.position)
        position[2] -= 0.1
        lowerNaHeight = excessCoolantHeight + 0.1
        self.surfaceCard = mcnpCF.getRHPRotated(flatToFlat, lowerNaHeight, position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity, self.surfaceNum,
                                             self.universe, cellComment)
