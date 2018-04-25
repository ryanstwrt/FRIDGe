import numpy as np
import pandas as pd
import os


def fuel_assembly_geometry_reader(pin_path):
    with open(pin_path, "r") as mat_file:
        pin_data = np.zeros(6)
        pin_materials = []
        assembly_data = np.zeros(6)
        assembly_materials = []
        plenum_data = np.zeros(1)
        plenum_materials = []
        fuel_reflector_data = np.zeros(1)
        fuel_reflector_materials = []
        for i, line in enumerate(mat_file):
            holder = [x for x in line.split(' ')]
            if 0 < i < 10:
                if i > 6:
                    pin_materials.append(holder[1])
                else:
                    pin_data[i-1] = holder[1]
            elif 11 < i < 20:
                if i > 17:
                    assembly_materials.append(holder[1])
                else:
                    assembly_data[i-12] = holder[1]
            elif 21 < i < 25:
                if i > 22:
                    plenum_materials.append(holder[1:])
                elif i == 22:
                    plenum_data[0] = holder[1]
            elif 26 < i < 30:
                if i > 27:
                    fuel_reflector_materials.append(holder[1:])
                else:
                    fuel_reflector_data[0] = holder[1]
    #fuel_assembly = pd.DataFrame()
    return

cur_dir = os.path.dirname(__file__)
pin_path = os.path.join(cur_dir, 'Geometry/A271.txt')

fuel_assembly_geometry_reader(pin_path)
