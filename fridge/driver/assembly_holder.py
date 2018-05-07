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


    def __init__(self, assembly_data, assembly_type, pin_data, assembly_universe):
        """
        Initializes the Assembly class with its corresponding data and assembly type

        args:
           assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
           assembly_type (str): string which tells what subclass of assembly to create
           pin_data (DataFram: data frame containing the data for the pin and pin type
           assembly_universe (int): the universe number which will be used for all parts of this assembly
        return:
            void
        """
        self.assembly_data = assembly_data
        self.assembly_type = assembly_type
        self.assembly_universe = assembly_universe
        self.surface_number = self.assembly_universe
        self.cell_number = self.assembly_universe + 50

        if assembly_type == 'fuel':
            self.pin = FuelPin(pin_data[0], pin_data[1], pin_data[2], pin_data[3])
            self.fuel_id = self.assembly_universe
            self.bond_id = self.assembly_universe + 1
            self.clad_id = self.assembly_universe + 2
            self.coolant_id = self.assembly_universe + 3


class Pin:
    """
        The Pin class holds all the information for a given pin type.
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
    def __init__(self, pin, fuel, bond, clad):
        super(FuelPin, self).__init__(pin)
        self.fuel_material = fuel
        self.fuel_bond = bond
        self.fuel_clad = clad
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
