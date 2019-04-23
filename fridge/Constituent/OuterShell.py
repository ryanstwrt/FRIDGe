import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class OuterShell(Constituent.Constituent):
    """The creates a shell around the assembly which allows the assembly to fit into a single universe."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, unitInfo):
        assemblyHeight = unitInfo[0]
        pitch = unitInfo[1]
        surfaceComment = "$Assembly: Full Assembly Surface"
        cellComment = "$Assembly"
        self.surfaceCard = mcnpCF.getRHPRotated(pitch, assemblyHeight, self.position, self.surfaceNum,
                                         surfaceComment)
        self.cellCard = mcnpCF.getAssemblyUniverseCell(self.surfaceNum, self.cellNum, self.universe, cellComment)
