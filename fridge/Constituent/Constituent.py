import fridge.Material.Material as materialReader
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class Constituent(object):
    """Base class for creating an assembly."""
    def __init__(self, unit_info, void_percent=1.0):
        """Initializes the data for creating a constituent."""
        self.universe = unit_info[0][0]
        self.cellNum = unit_info[0][1]
        self.surfaceNum = unit_info[0][2]
        self.materialXCLibrary = unit_info[0][4]
        self.position = unit_info[0][5]
        self.materialNum = unit_info[0][6]
        self.voidPercent = void_percent
        self.surfaceCard = ''
        self.cellCard = ''
        self.materialCard = ''
        self.material = None

    def get_material_card(self, material_name):
        """Creates the material for the given constituent and creates the material card."""
        self.material = materialReader.Material()
        self.material.set_material(material_name)
        if self.voidPercent != 1.0:
            self.material.set_void(self.voidPercent)
        self.materialCard = mcnpCF.getMaterialCard(self.material, self.materialXCLibrary, self.materialNum)

    def make_component(self, unit_info):
        """Creates the component for the given constituent and creates the cell/surface cards."""
        pass
