from FRIDGe.fridge.Constituent import Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class OuterShell(Constituent.Constituent):
    def __init__(self, unitInfo):
        self.reflectorHeight = unitInfo[1][0]
        self.fuelHeight = unitInfo[1][1] * 1.01
        self.plenumHeight = unitInfo[1][2]
        self.assemblyHeight = unitInfo[1][3]
        self.pitch = unitInfo[1][4]
        self.assemblyPosition = unitInfo[1][5]
        self.definedHeight = 2 * self.reflectorHeight + self.fuelHeight + self.plenumHeight
        self.excessNaHeight = (self.assemblyHeight - self.definedHeight) / 2
        self.positionBottomAssembly = mcnpCF.getPosition(self.assemblyPosition, self.pitch,
                                                         -(self.reflectorHeight + self.excessNaHeight))
        self.positionTopUpperReflector = mcnpCF.getPosition(self.assemblyPosition, self.pitch,
                                                            self.definedHeight - self.reflectorHeight)
        super().__init__(unitInfo)
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, unitInfo):
        surfaceComment = "$Assembly: Full Assembly Surface"
        cellComment = "$Assembly"
        self.surfaceCard = mcnpCF.getRHP(self.pitch, self.assemblyHeight, self.positionBottomAssembly, self.surfaceNum,
                                         surfaceComment)
        self.cellCard = mcnpCF.getAssemblyUniverseCell(self.surfaceNum, self.cellNum, self.universe, cellComment)
