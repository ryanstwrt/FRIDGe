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
           assembly_universe (int): the universe number which will be used for all parts of this assembly
        return:
            void
        """
        # Potentially throw these three functions into the assembly holder and unpack them when they are needed.
        self.assembly_data = assembly_data
        self.plenum_data = plenum_data
        self.fuel_reflector_data = fuel_reflector_data
        self.assembly_universe = assembly_universe
        self.universe_counter = assembly_universe
        self.surface_number = self.assembly_universe
        self.cell_number = self.assembly_universe + 50
        self.assembly_id = self.assembly_universe + 20
        self.assembly_coolant_id = self.assembly_universe + 21
        self.lower_reflector_surface = ''
        self.plenum_surface = ''
        self.upper_reflector_surface = ''
        self.inner_duct_surface = ''
        self.outer_duct_surface = ''
        self.universe_surface = ''
        self.lower_reflector_mcnp_surface = ''
        self.plenum_mcnp_surface = ''
        self.upper_reflector_mcnp_surface = ''
        self.inner_duct_mcnp_surface = ''
        self.outer_duct_mcnp_surface = ''
        self.universe_mcnp_surface = ''

        # Characteristics for a fuel pin
        self.pin = FuelPin(fuel_data)
        self.fuel_id = self.assembly_universe + 22
        self.bond_id = self.assembly_universe + 23
        self.clad_id = self.assembly_universe + 24
        self.coolant_id = self.assembly_universe + 25
        self.fuel_reflector_id = self.assembly_universe + 26



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
            fuel_pellet_surface (str): The surface number for the fuel pellet
            fuel_bond_surface (str): The surface number for the bond
            fuel_clad_surface (str): The surface number for the clad
            fuel_pin_universe_surface (str): The surface number for the coolant pin universe
            fuel_pellet_mcnp_surface (str): The mcnp line for the fuel pellet
            fuel_bond_mcnp_surface (str): The mcnp line for the bond
            fuel_clad_mcnp_surface (str): The mcnp line for the clad
            fuel_pin_universe_mcnp_surface (str): The mcnp line for the coolant pin universe
            fuel_pellet_cell (str): The cell number for the fuel pellet
            fuel_bond_cell (str): The cell number for the bond
            fuel_clad_cell (str): The cell number for the clad
            fuel_universe_cell (str): The cell number for the coolant pin universe
            fuel_pellet_mcnp_cell (str): The mcnp line number for the fuel pellet
            fuel_bond_mcnp_cell (str): The mcnp line number for the bond
            fuel_clad_mcnp_cell (str): The mcnp line number for the clad
            fuel_universe_mcnp_cell (str): The mcnp line number for the coolant pin universe
    """

    def __init__(self, fuel):
        fuel_material_fuel = mat_read.material_reader([fuel.ix['fuel', 'fuel']])
        fuel_material_bond = mat_read.material_reader([fuel.ix['bond', 'fuel']])
        fuel_material_cladding = mat_read.material_reader([fuel.ix['clad', 'fuel']])

        super().__init__(fuel)
        self.fuel_material = fuel_material_fuel
        self.fuel_bond = fuel_material_bond
        self.fuel_clad = fuel_material_cladding
        self.pin_cell_universe = ''
        self.blank_cell_universe = ''
        self.fuel_pellet_surface = ''
        self.fuel_bond_surface = ''
        self.fuel_clad_surface = ''
        self.fuel_pin_universe_surface = ''
        self.fuel_pellet_mcnp_surface = ''
        self.fuel_bond_mcnp_surface = ''
        self.fuel_clad_mcnp_surface = ''
        self.fuel_pin_universe_mcnp_surface = ''
        self.fuel_pellet_cell = ''
        self.fuel_bond_cell = ''
        self.fuel_clad_cell = ''
        self.fuel_universe_cell = ''
        self.fuel_pellet_mcnp_cell = ''
        self.fuel_bond_mcnp_cell = ''
        self.fuel_clad_mcnp_cell = ''
        self.fuel_universe_mcnp_cell = ''
        self.na_cell = ''
        self.na_mcnp_cell = ''
