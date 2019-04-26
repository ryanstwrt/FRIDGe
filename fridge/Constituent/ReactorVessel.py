import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as MCF


class ReactorVessel(Constituent.Constituent):
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.vesselRadius = unitInfo[1][0]
        self.vesselHeight = unitInfo[1][1]
        self.coreCoolantSurfaceNum = unitInfo[1][2]
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent([1])

    def makeComponent(self, unitInfo):
        self.surfaceCard = MCF.getRCC(self.vesselRadius, self.vesselHeight, self.position, self.surfaceNum,
                                      '$Vessel surrounding the core')
        self.cellCard = MCF.getConcentricCellCoolant(self.cellNum, self.materialNum, self.material.atomDensity,
                                                     [self.coreCoolantSurfaceNum], self.surfaceNum, '$Reactor Vessel')
