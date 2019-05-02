import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class OuterShell(Constituent.Constituent):
    """The creates a shell around the assembly which allows the assembly to fit into a single universe."""
    def __init__(self, unit_info):
        super().__init__(unit_info)
        self.get_material_card(unit_info[0][3])
        self.make_component(unit_info[1])

    def make_component(self, unit_info):
        assembly_height = unit_info[0]
        pitch = unit_info[1]
        surface_comment = "$Assembly: Full Assembly Surface"
        cell_comment = "$Assembly"
        self.surfaceCard = mcnpCF.build_rotated_right_hexagonal_prism_surface(pitch, assembly_height, self.position,
                                                                              self.surfaceNum, surface_comment)
        self.cellCard = mcnpCF.build_assembly_universe_cell(self.surfaceNum, self.cellNum, self.universe, cell_comment)
