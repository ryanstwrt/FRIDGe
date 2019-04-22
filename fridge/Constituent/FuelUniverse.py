import fridge.Constituent.Constituent as Constituent
import numpy as np


class FuelUniverse(Constituent.Constituent):
    """Creates the lattice for the fuel pin, bond, clad, and coolant.
    This lattice gets repeated for the number of pins present, and all excess pins are BlankCoolant."""
    def __init__(self, fuelUniverseInfo):
        self.fuelUniverse = fuelUniverseInfo[0]
        self.blankUniverse = fuelUniverseInfo[1]
        self.numPins = fuelUniverseInfo[2]
        self.cellNum = fuelUniverseInfo[3]
        self.blankCellNum = fuelUniverseInfo[4]
        self.latticeUniverse = fuelUniverseInfo[5]
        self.cellCard = self.getCellCard()

    def getCellCard(self):
        cellCard = "{} 0 -{} lat=2 u={} imp:n=1\n".format(self.cellNum, self.blankCellNum, self.latticeUniverse)
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

        cellCard += "     fill=-{}:{} -{}:{} 0:0\n     ".format(rings, rings, rings, rings)
        row_jump = 0
        for row in lattice_array:
            for lat_iter, element in enumerate(row):
                if (row_jump+1) % 10 == 0:
                    cellCard += " {}\n     ".format(int(element))
                else:
                    cellCard += " {}".format(int(element))
                row_jump += 1
        return cellCard
