import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class OuterShell(Constituent.Constituent):
    """The creates a shell around the assembly which allows the assembly to fit into a single universe."""
    def __init__(self, unitInfo):
        self.positionBottomAssembly = unitInfo[1][0]
        self.assemblyHeight = unitInfo[1][1]
        self.pitch = unitInfo[1][2]
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, unitInfo):
        surfaceComment = "$Assembly: Full Assembly Surface"
        cellComment = "$Assembly"
        self.surfaceCard = mcnpCF.getRHP(self.pitch, self.assemblyHeight, self.positionBottomAssembly, self.surfaceNum,
                                         surfaceComment)
        self.cellCard = mcnpCF.getAssemblyUniverseCell(self.surfaceNum, self.cellNum, self.universe, cellComment)
