import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Duct(Constituent.Constituent):
    """Encompasses the reflector, plenum, and fuel region in a hexagon duct."""
    def __init__(self, unitInfo):
        super().__init__(unitInfo)
        self.flat2flat = 0
        self.height = 0
        self.innerSurfaceNum = 0
        self.getMaterialCard(unitInfo[0][3])
        self.makeComponent(unitInfo[1])

    def makeComponent(self, ductInfo):
        self.flat2flat = ductInfo[0]
        self.height = ductInfo[1]
        self.innerSurfaceNum = ductInfo[2]
        surfaceComment = "$Assembly: Duct Outer Surface"
        cellComment = "$Assembly: Assembly Duct"
        self.surfaceCard = mcnpCF.getRHPRotated(self.flat2flat, self.height, self.position, self.surfaceNum, surfaceComment)
        self.cellCard = mcnpCF.getConcentricCell(self.cellNum, self.materialNum, self.material.atomDensity,
                                                 self.innerSurfaceNum, self.surfaceNum, self.universe, cellComment)
