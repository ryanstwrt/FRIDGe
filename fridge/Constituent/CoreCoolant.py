import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as MCF


class CoreCoolant(Constituent.Constituent):
    def __init__(self, unitInfo, voidPercent=1.0):
        super().__init__(unitInfo, voidPercent=voidPercent)
        self.coolantRadius = unitInfo[1][0]
        self.coolantHeight = unitInfo[1][1]
        self.assemblySurfaceList = unitInfo[1][2]
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent([1])

    def makeComponent(self, unitInfo):
        self.surfaceCard = MCF.getRCC(self.coolantRadius, self.coolantHeight, self.position,
                                             self.surfaceNum, '$Coolant Surrounding Assemblies')
        self.cellCard = MCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                            self.assemblySurfaceList, self.surfaceNum, '',
                                                            '$Coolant Surrounding Assemblies')
