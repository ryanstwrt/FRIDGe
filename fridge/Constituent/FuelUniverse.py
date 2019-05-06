import fridge.Constituent.Constituent as Constituent
import numpy as np


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
        self.cellCard = self.make_cell_card()

    def make_cell_card(self):
        cell_card = "{} 0 -{} lat=2 u={} imp:n=1\n".format(self.cellNum, self.blankCellNum, self.latticeUniverse)
        rings = int(max(np.roots([1, -1, -2*(self.numPins-1)/6])))
        lattice_array = np.zeros((rings * 2 + 1, rings * 2 + 1))
        for x in range(rings * 2 + 1):
            for y in range(rings * 2 + 1):
                if x == 0 or x == 2 * rings:
                    lattice_array[x][y] = self.blankUniverse
                elif x < (rings + 1):
                    if y < (rings + 1 - x) or y == (2 * rings):
                        lattice_array[x][y] = self.blankUniverse
                    else:
                        lattice_array[x][y] = self.fuelUniverse
                else:
                    if y > (2 * rings - (x - rings + 1)) or y == 0:
                        lattice_array[x][y] = self.blankUniverse
                    else:
                        lattice_array[x][y] = self.fuelUniverse

        cell_card += "     fill=-{}:{} -{}:{} 0:0\n     ".format(rings, rings, rings, rings)
        row_jump = 0
        for row in lattice_array:
            for lat_iter, element in enumerate(row):
                if (row_jump+1) % 10 == 0:
                    cell_card += " {}\n     ".format(int(element))
                else:
                    cell_card += " {}".format(int(element))
                row_jump += 1
        return cell_card
