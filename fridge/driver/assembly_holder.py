from FRIDGe.fridge.input_readers import material_reader as mat_read


class Assembly:
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

    def __init__(self, assembly_data, plenum_data, fuel_reflector_data, fuel_data, assembly_universe):
        """
        Initializes the Assembly class with its corresponding data and assembly type

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
        """
        #plenum_material = mat_read.material_reader([plenum_data.ix['fuel', 'fuel']])
        #plenum_material = mat_read.material_reader([plenum_data.ix['fuel', 'fuel']])
        #fuel_reflecor_material = mat_read.material_reader([fuel_reflector_data.ix['bond', 'fuel']])

        # Potentially throw these three functions into the assembly holder and unpack them when they are needed.
        self.assembly_material = mat_read.material_reader([assembly_data.ix['assembly', 'assembly']])
        self.assembly_data = assembly_data
        self.plenum_data = plenum_data
        self.fuel_reflector_data = fuel_reflector_data
        self.assembly_id = self.assembly_universe + 20
        self.assembly_coolant_id = self.assembly_universe + 21
        self.assembly_universe = assembly_universe
        self.universe_counter = assembly_universe
        self.surface_number = self.assembly_universe
        self.cell_number = self.assembly_universe + 50
        self.latice_universe = 0

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

        self.lattice_holder_mcnp_cell = 0
        self.lattice_mcnp_cell = ''

        # Characteristics for a fuel pin
        self.pin = FuelPin(fuel_data)
        self.fuel_id = self.assembly_universe + 22
        self.bond_id = self.assembly_universe + 23
        self.clad_id = self.assembly_universe + 24
        self.coolant_id = self.assembly_universe + 25
        self.fuel_reflector_id = self.assembly_universe + 26
        self.plenum_id = self.assembly_universe + 27


class Pin:
    """
        The Pin class holds all the information for a given pin type.

        Attributes:
            pin_data (DataFrame): data frame containing the data for the pin and pin type
    """

    def __init__(self, pin_data):
        """
        Initializes the Assembly class with its corresponding data and assembly type

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
        self.fuel_pin_universe = 0

        self.fuel_universe_surface = 0
        self.fuel_universe_mcnp_surface = ''
        self.fuel_universe_cell = 0
        self.fuel_universe_mcnp_cell = ''

        self.na_cell_universe = 0
        self.na_cell = 0
        self.na_mcnp_cell = ''

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
