import fridge.Constituent.Constituent as Constituent
import fridge.utilities.mcnpCreatorFunctions as mcnpCF


class FuelUniverse(Constituent.Constituent):
    """Creates the lattice for the fuel pin, bond, clad, and coolant.

    This lattice gets repeated for the number of pins present, and all excess pins are BlankCoolant."""
    def __init__(self, fuel_universe_info):
        self.fuelUniverse = fuel_universe_info[0]
        self.blankUniverse = fuel_universe_info[1]
        self.numPins = fuel_universe_info[2]
        self.cellNum = fuel_universe_info[3]
        self.blankCellNum = fuel_universe_info[4]
        self.latticeUniverse = fuel_universe_info[5]
        self.cellCard = mcnpCF.build_hexagonal_lattice_cell(self.cellNum, self.blankCellNum, self.latticeUniverse,
                                                            self.numPins, self.blankUniverse, self.fuelUniverse)
