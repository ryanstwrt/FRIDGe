import os
import glob
import yaml


class global_variables():
    """
    This class will hold all the variables that are not specific to a single assembly.
    """
    def __init__(self, assembly_name):
        self.assembly_file_name = assembly_name + '_Assembly'
        self.xc_set = '.82c'
        self.universe = 100
        self.number_assemblies = 1
        self.na_voiding = False
        self.temperature = 0
        self.temp_adjusted_density = False
        self.temp_adjusted_volume = False
        self.clad_smear = False
        self.bond_smear = False
        self.void_per = 0
        self.assembly_type = ''

        self.read_input_file()

    def read_input_file(self):
        cur_dir = os.path.dirname(__file__)
        input_dir = os.path.join(cur_dir, "../fridge_input_file")
        assembly_file = glob.glob(os.path.join(input_dir, self.assembly_file_name + '.*'))

        with open(assembly_file[0], "r") as file:
            inputs = yaml.safe_load(file)
        self.assembly_type = inputs["Assembly Type"]
        self.number_assemblies = int(inputs["Number of Assemblies"])
        self.na_voiding = bool(inputs["Na Voiding"])
        self.temperature = float(inputs["Temperature"])
        self.temp_adjusted_density = bool(inputs["Temperature Adjusted Density"])
        self.temp_adjusted_volume = bool(inputs["Temperature Adjusted Volume"])
        self.clad_smear = bool(inputs["Smear Clad"])
        self.bond_smear = bool(inputs["Smear Bond"])

        if self.na_voiding:
            if "Void Percent" in inputs:
                self.void_per = float(inputs["Void Percent"])
            else:
                print("Sodium voiding requires 'Void Percent:' in the input file")
