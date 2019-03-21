import FRIDGe.fridge.utilities.materialReader as materialReader
import FRIDGe.fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Constituent(object):
    def __init__(self, unitInfo):
        self.universe = unitInfo[0][0]
        self.surfaceNum = unitInfo[0][1]
        self.cellNum = unitInfo[0][2]
        self.materialXCLibrary = unitInfo[0][4]
        self.position = unitInfo[0][5]
        self.materialNum = unitInfo[0][6]
        self.surfaceCard = ''
        self.cellCard = ''
        self.materialCard = ''
        self.material = None

    def getMaterialCard(self, materialName):
        self.material = materialReader.Material()
        self.material.setMaterial(materialName)
        self.materialCard = mcnpCF.getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)

    def makeComponent(self, unitInfo):
        pass
