import FRIDGe.fridge.Constituent.Constituent as Constituent
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Smear(Constituent.Constituent):
    """Creates a constituent which is a smear of materials."""
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][1]
        self.cellNum = unitInfo[0][2]
        self.materialXCLibrary = unitInfo[0][4]
        self.material = unitInfo[0][3]
        self.position = unitInfo[0][5]
        self.materialNum = unitInfo[0][6]
        self.componentName = unitInfo[2]
        self.material = mcnpCF.getSmearedMaterial(self.material, self.materialXCLibrary, self.materialNum)
        self.makeComponent(unitInfo[1])
        self.getMaterialCard(self.material)
        self.flat2flat = 0
        self.height = 0

    def makeComponent(self, ductInfo):
        self.flat2flat = ductInfo[0]
        self.height = ductInfo[1]
        surfaceComment = "$Assembly: {}".format(self.componentName)
        cellComment = "$Assembly: {}".format(self.componentName)
        self.surfaceCard = mcnpCF.getRHP(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getSingleCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                             self.surfaceNum, self.universe, cellComment)

    def getMaterialCard(self, materialName):
        self.materialCard = mcnpCF.getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)
