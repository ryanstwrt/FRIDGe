import fridge.Material.Material as materialReader
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Constituent(object):
    """Base class for creating an assembly."""
    def __init__(self, unitInfo, voidPercent=1.0):
        """Initializes the data for creating a constituent."""
        self.universe = unitInfo[0][0]
        self.cellNum = unitInfo[0][1]
        self.surfaceNum = unitInfo[0][2]
        self.materialXCLibrary = unitInfo[0][4]
        self.position = unitInfo[0][5]
        self.materialNum = unitInfo[0][6]
        self.voidPercent = voidPercent
        self.surfaceCard = ''
        self.cellCard = ''
        self.materialCard = ''
        self.material = None

    def getMaterialCard(self, materialName):
        """Creates the material for the given constituent and creates the material card."""
        self.material = materialReader.Material()
        self.material.setMaterial(materialName)
        if self.voidPercent != 1.0:
            self.material.voidMaterial(self.voidPercent)
        self.materialCard = mcnpCF.getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)

    def makeComponent(self, unitInfo):
        """Creates the component for the given constituent and creates the cell/surface cards."""
        pass
