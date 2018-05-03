
class Assembly:
    """
        The assembly class holds all of the information regarding the assembly that is currently being built.
    """

    def __init__(self, assembly_data, assembly_type, pin_data):
        """
        Initializes the Assembly class with its corresponding data and assembly type

        args:
           assembly_data (DataFrame): data frame which holds all of the information regarding the assembly
           assembly_type (str): string which tells what subclass of assembly to create
        return:
            void
        """
        self.assembly_data = assembly_data
        self.assembly_type = assembly_type
        if assembly_type == 'fuel':
            self.pin = FuelPin(pin_data[0], pin_data[1], pin_data[2], pin_data[3])


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
    """
    def __init__(self, pin, fuel, bond, clad):
        self.fuel_material = fuel
        self.fuel_bond = bond
        self.fuel_clad = clad
        super(FuelPin, self).__init__(pin)
