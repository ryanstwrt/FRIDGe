from FRIDGe.fridge.Constituent import Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class InnerDuct(Constituent.Constituent):
    def __init__(self, ductInfo):
        self.universe = ductInfo[0]
        self.cellNum = ductInfo[1]
        self.surfaceNum = ductInfo[2]
        self.assemblyUniverse = ductInfo[3]
        self.latticeUniverse = ductInfo[4]
        self.position = ductInfo[5]
        self.flat2flat = ductInfo[6]
        self.height = ductInfo[7] * 1.01
        self.makeComponent()

    def makeComponent(self):
        surfaceComment = "$Assembly: Duct Inner Surface"
        cellComment = "$Assembly: Inner Portion of Assembly"
        self.surfaceCard = mcnpCF.getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getFuelLatticeCell(self.cellNum, self.surfaceNum, self.assemblyUniverse,
                                                  self.latticeUniverse, cellComment)
