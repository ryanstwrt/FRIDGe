from FRIDGe.fridge.utilities import geometry_reader as geo_read, material_reader as mat_read


class FuelAssembly:
    """
        The assembly class holds all of the information regarding the assembly that is currently being built.

    args:

    Attributes:
        assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
        assembly_type (str): string which tells what subclass of assembly to create
        pin_data (DataFram: data frame containing the data for the pin and pin type
        assembly_universe (int): the universe number which will be used for all parts of this assembly
        surface_number (int): based on the universe number, keeps track of the surface number when surfcae is built
        cell_number (int): based on the universe number, keeps track of the cell number when cell is built

        fuel assembly:
            fuel_id (int): id number for the fuel material
            bond_id (int): id number for the bond material
            clad_id (int): id number for the clad material
            coolant_id (int): id number for the coolant material
    """

    def __init__(self, gloabl_vars, assembly_type):
        """
        Initializes the FuelAssembly class with its corresponding data and assembly type

        args:
           assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
           assembly_type (str): string which tells what subclass of assembly to create
           pin_data (DataFram: data frame containing the data for the pin and pin type
           assembly_id (int): material id number for the assembly cladding
           assembly_coolant_id (int) material id number for the coolant outisde the assembly
           assembly_universe (int): the universe number which will be used for all parts of the assembly
        attributes:
            assembly_material (2D Array): Contains both the array of ZAIDS contained in the assembly cladding and the atom density
            assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
            plenum_data (DataFrame): data frame which holds all of the information regarding the plenum
            fuel_reflector_data(DataFrame): data frame which holds all of the information regarding the fuel reflector
            assembly_id (int): material number for the assembly
            assembly_coolant_id (int): material number for the coolant
            assembly_universe (int): universe number assigned to the assembly
            universe_counter (int): keeps track of the universe number within the assembly
            surface_number (int): keeps track of the surface number within the assembly
            cell_number (int): keeps track of the cell number within the assembly
            lattice_universe (int): universe number assigned to the lattice construct
            lower_reflector_surface (int): surface number assigned to the lower reflector
            lower_reflector_mcnp_surface (str): MCNP surface card for the lower reflector
            lower_reflector_cell (int): cell number assigned to the lower reflector
            lower_reflector_mcnp_cell (str): MCNP cell card for the lower reflector
            plenum_surface (int): surface number assigned to the plenum
            plenum_mcnp_surface (str): MCNP surface card for the plenum
            plenum_cell (int): cell number assigned to the plenum
            plenum_mcnp_cell (str): MCNP cell card for the plenum
            upper_reflector_surface (int): surface number assigned to upper reflector
            upper_reflector_mcnp_surface (str): MCNP surface card for the upper reflector
            upper_reflector_cell (int): cell number assigned to the lower reflector
            upper_reflector_mcnp_cell (str): MCNP cell card for the lower reflector
            inner_duct_surface (int): surface number assigned to inner duct
            inner_duct_mcnp_surface (str): MCNP surface card for the inner duct
            inner_duct_cell (int): cell number assigned to the inner duct
            inner_duct_mcnp_cell (str): MCNP cell card for the inner duct
            outer_duct_surface (int): surface number assigned to outer duct
            outer_duct_mcnp_surface (str): MCNP surface card for the outer duct
            outer_duct_cell (int): cell number assigned to the outer duct
            outer_duct_mcnp_cell (str): MCNP cell card for the outer duct
            universe_surface (int): surface number assigned assembly universe
            universe_mcnp_surface (str): MCNP surface card for assembly universe
            universe_cell (int): cell number assigned to the assembly universe
            universe_mcnp_cell (str): MCNP cell card for the assembly universe
            lower_plane_surface (int): surface number for lower plane (only used in single assembly)
            lower_plane_surface_mcnp (str): MCNP surface card for lower plane
            upper_plane_surface (int): surface number for upper plane (only used in single assembly)
            upper_plane_surface_mcnp (str): MCNP surface card for upper plane
            lattice_mcnp_cell (int): cell number fo the lattice holder
            lattice_holder_mcnp_cell (str): MCNP cell card for where the lattice construct will be palced

            pin (class): creates a pin class which determine what type of pin will be used in the assembly
            fuel_id (int): material number for the fuel
            bond_id (int): material number for the bond
            clad_id (int): material number for the clad
            coolant_id (int): material number for the coolant
            fuel_reflector_id (int): material number for the fuel reflector
            plenum_id (int): material number for the plenum

        return:
            void
            :param assembly_type:
            :param gloabl_vars:
        """
        fuel_data, assembly_data, plenum_data, fuel_reflector_data = \
            geo_read.fuel_assembly_geometry_reader(assembly_type)

        self.plenum_smear_per = [plenum_data.ix['coolant_per', 'plenum'],
                                 plenum_data.ix['void_per', 'plenum'],
                                 plenum_data.ix['clad_per', 'plenum']]
        self.plenum_smear_zaids = [plenum_data.ix['coolant', 'plenum'],
                                   plenum_data.ix['void', 'plenum'],
                                   plenum_data.ix['clad', 'plenum']]
        self.plenum_material = []
        self.fuel_reflector_material = []

        self.fuel_reflector_smear_per = [fuel_reflector_data.ix['coolant_per', 'fuel_reflector'],
                                         fuel_reflector_data.ix['clad_per', 'fuel_reflector']]
        self.fuel_reflector_smear_zaids = [fuel_reflector_data.ix['coolant', 'fuel_reflector'],
                                           fuel_reflector_data.ix['clad', 'fuel_reflector']]

        # Potentially throw these three functions into the assembly holder and unpack them when they are needed.
        self.assembly_material = mat_read.material_reader([assembly_data.ix['assembly', 'assembly']])
        self.assembly_data = assembly_data
        self.plenum_data = plenum_data
        self.fuel_reflector_data = fuel_reflector_data
        self.assembly_universe = gloabl_vars.universe
        self.assembly_id = self.assembly_universe + 20
        self.assembly_coolant_id = self.assembly_universe + 21
        self.universe_counter = self.assembly_universe
        self.surface_number = self.assembly_universe
        self.cell_number = self.assembly_universe + 50
        self.material_number = self.assembly_universe + 50
        self.lattice_universe = 0

        self.lower_reflector_surface = 0
        self.lower_reflector_mcnp_surface = ''
        self.lower_reflector_cell = 0
        self.lower_reflector_mcnp_cell = 0
        self.plenum_surface = 0
        self.plenum_mcnp_surface = ''
        self.plenum_cell = 0
        self.plenum_mcnp_cell = 0
        self.upper_reflector_surface = 0
        self.upper_reflector_mcnp_surface = ''
        self.upper_reflector_cell = 0
        self.upper_reflector_mcnp_cell = 0
        self.inner_duct_surface = 0
        self.inner_duct_mcnp_surface = ''
        self.inner_duct_cell = 0
        self.inner_duct_mcnp_cell = ''
        self.outer_duct_surface = 0
        self.outer_duct_mcnp_surface = ''
        self.outer_duct_cell = 0
        self.outer_duct_mcnp_cell = ''
        self.universe_surface = 0
        self.universe_mcnp_surface = ''
        self.universe_cell = 0
        self.universe_mcnp_cell = ''
        self.lower_plane_surface = 0
        self.lower_plane_surface_mcnp = ''
        self.upper_plane_surface = 0
        self.upper_plane_surface_mcnp = ''

        self.lattice_holder_mcnp_cell = ''
        self.lattice_holder_cell = 0
        self.lattice_mcnp_cell = ''
        self.void_mcnp_cell = ''

        # Characteristics for a fuel pin
        self.pin = FuelPin(fuel_data)
        self.material = Material()
        self.fuel_id = self.assembly_universe + 22
        self.bond_id = self.assembly_universe + 23
        self.clad_id = self.assembly_universe + 24
        self.coolant_id = self.assembly_universe + 25
        self.fuel_reflector_id = self.assembly_universe + 26
        self.plenum_id = self.assembly_universe + 27

        self.k_card = ''


class Pin:
    """
        The Pin class holds all the information for a given pin type.

        Attributes:
            pin_data (DataFrame): data frame containing the data for the pin and pin type
    """

    def __init__(self, pin_data):
        """
        Initializes the FuelAssembly class with its corresponding data and assembly type

        args:
           pin_data (DataFrame): data frame which holds all of the information regarding the pin
        return:
            void
        """
        self.pin_data = pin_data


class FuelPin(Pin):
    """
        A pin subclass that holds information for a fuel type pin
        This class holds surface/cell numbers, MCNP input file formats

        args:
            Pin (Class):

        Attributes:
            fuel_material (2D array): Contains both the array of ZAIDS contained in the fuel and the atom density
            fuel_bond (2D array): Contains both the array of ZAIDS contained in the bond and the atom density
            fuel_clad (2D array): Contains both the array of ZAIDS contained in the clad and the atom density

            fuel_pellet_surface (int): The surface number for the fuel pellet
            fuel_pellet_mcnp_surface (str): The mcnp line for the fuel pellet
            fuel_pellet_cell (int): The cell number for the fuel pellet
            fuel_pellet_mcnp_cell (str): The mcnp line number for the fuel pellet
            fuel_bond_surface (int): The surface number for the bond
            fuel_bond_mcnp_surface (str): The mcnp line for the bond
            fuel_bond_cell (int): The cell number for the bond
            fuel_bond_mcnp_cell (str): The mcnp line number for the bond
            fuel_clad_surface (int): The surface number for the clad
            fuel_clad_mcnp_surface (str): The mcnp line for the clad
            fuel_clad_cell (int): The cell number for the clad
            fuel_clad_mcnp_cell (str): The mcnp line number for the clad
            fuel_universe_surface (int): The surface number for the coolant pin universe
            fuel_universe_mcnp_surface (str): The mcnp line for the coolant pin universe
            fuel_universe_cell (int): The cell number for the coolant pin universe
            fuel_universe_mcnp_cell (str): The mcnp line number for the coolant pin universe
    """

    def __init__(self, fuel):
        super().__init__(fuel)
        self.fuel_material = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
        self.fuel_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
        self.fuel_clad = mat_read.material_reader([fuel.ix['clad', 'fuel']])
        self.wire_wrap_smear_zaids = [fuel.ix['clad', 'fuel'],
                                      fuel.ix['bond', 'fuel']]
        self.wire_wrap_smear_per = []
        self.fuel_pin_universe = 0

        self.fuel_universe_surface = 0
        self.fuel_universe_mcnp_surface = ''
        self.fuel_universe_cell = 0
        self.fuel_universe_mcnp_cell = ''

        self.fuel_pellet_surface = 0
        self.fuel_pellet_mcnp_surface = ''
        self.fuel_pellet_cell = 0
        self.fuel_pellet_mcnp_cell = ''

        self.fuel_bond_surface = 0
        self.fuel_bond_mcnp_surface = ''
        self.fuel_bond_cell = 0
        self.fuel_bond_mcnp_cell = ''

        self.fuel_clad_surface = 0
        self.fuel_clad_mcnp_surface = ''
        self.fuel_clad_cell = 0
        self.fuel_clad_mcnp_cell = ''

        self.na_cell_universe = 0
        self.na_cell = 0
        self.na_mcnp_cell = ''
        self.na_cell_surface = 0
        self.na_cell_mcnp_surface = ''



class Material:
    """
        Class which will hold all of the material information regarding an assembly.
    """

    def __init__(self):
        self.fuel_num = 0
        self.fuel = []
        self.fuel_xc_set = '.82c'
        self.fuel_mcnp_data = ''

        self.bond_num = 0
        self.bond = []
        self.bond_xc_set = '.82c'
        self.bond_mcnp_data = ''

        self.clad_num = 0
        self.clad = []
        self.clad_xc_set = '.82c'
        self.clad_mcnp_data = ''

        self.coolant_num = 0
        self.coolant = []
        self.coolant_xc_set = '.82c'
        self.coolant_mcnp_data = ''

        self.wire_wrap_smear_num = 0
        self.wire_wrap_smear = []
        self.wire_wrap_smear_xc_set = '.82c'
        self.wire_wrap_smear_mcnp_data = ''

        self.assembly_num = 0
        self.assembly = []
        self.assembly_xc_set = '.82c'
        self.assembly_mcnp_data = ''

        self.assembly_coolant_num = 0
        self.assembly_coolant = []
        self.assembly_coolant_xc_set = '.82c'
        self.assembly_coolant_mcnp_data = ''

        self.plenum_num = 0
        self.plenum = []
        self.plenum_xc_set = '.82c'
        self.plenum_mcnp_data = ''

        self.fuel_reflector_num = 0
        self.fuel_reflector = []
        self.fuel_reflector_xc_set = '.82c'
        self.fuel_reflector_mcnp_data = ''
