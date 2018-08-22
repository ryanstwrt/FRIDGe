import os
import glob
import yaml


class global_variables():
    """
    This class will hold all the variables that are not specific to a single assembly.
    """
    def __init__(self, assembly_name):
        self.assembly_file_name = assembly_name
        self.xc_library = ''
        self.xc_set = ''
        self.universe = 100
        self.cellNumber = 100
        self.surfaceNumber = 100
        self.materialNumber = 10
        self.number_assemblies = 1
        self.na_voiding = False
        self.temperature = 0
        self.temp_adjusted_density = False
        self.temp_adjusted_volume = False
        self.clad_smear = False
        self.bond_smear = False
        self.void_per = 0
        self.assembly_type = ''
        self.number_generations = 0
        self.number_skipped_generations = 0
        self.number_particles_generation = 0
        self.kopts = False
        self.ksens = False
        self.output_name = ''

        self.read_input_file()

    def read_input_file(self):
        cur_dir = os.path.dirname(__file__)
        input_dir = os.path.join(cur_dir, "../fridge_input_file")
        assembly_file = glob.glob(os.path.join(input_dir, self.assembly_file_name + '.*'))

        with open(assembly_file[0], "r") as file:
            inputs = yaml.safe_load(file)

        self.assembly_type = inputs["Fuel Assembly Type"]
        self.number_assemblies = int(inputs["Number of Assemblies"]) \
            if 'Number of Assemblies' in inputs else 1
        self.na_voiding = bool(inputs["Na Voiding"]) \
            if 'Na Voiding' in inputs else False
        self.temperature = float(inputs["Temperature"]) \
            if 'Temperature' in inputs else 900
        self.temp_adjusted_density = bool(inputs["Temperature Adjusted Density"]) \
            if 'Temperature Adjusted Density' in inputs else False
        self.temp_adjusted_volume = bool(inputs["Temperature Adjusted Volume"]) \
            if 'Temperature Adjusted Volume' in inputs else False
        self.clad_smear = bool(inputs["Smear Clad"]) \
            if 'Smear Bond' in inputs else False
        self.bond_smear = bool(inputs["Smear Bond"]) \
            if 'Smear Bond' in inputs else False
        self.xc_set = inputs["XC Set"] \
            if 'XC Set' in inputs else ''
        self.number_generations = int(inputs["Number of Generations"]) \
            if 'Number of Generations' in inputs else 230
        self.number_skipped_generations = int(inputs["Number of Skipped Generations"]) \
            if 'Number of Skipped Generations' in inputs else 30
        self.number_particles_generation = int(inputs["Number of Particles Per Generation"]) \
            if 'Number of Particle per Generation' in inputs else int(1e6)
        self.kopts = bool(inputs["kopts"]) \
            if 'kopts' in inputs else False
        self.void_per = float(inputs["Void Percent"]) \
            if "Void Percent" in inputs else 0
        self.output_name = inputs["Output File Name"] \
            if "Output File Name" in inputs else 'FRIDGe1'

        # Set the XC set depending on the temperature
        if self.temperature == 600:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.81c'
            elif self.xc_set == 'ENDFVII.0':
                self.xc_set = '.71c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.34c'
        elif self.temperature == 900:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.82c'
            elif self.xc_set == 'ENDFVII.0':
                self.xc_set = '.72c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.37c'
        elif self.temperature == 1200:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.83c'
            elif self.xc_set == 'ENDFVII.0':
                self.xc_set = '.73c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.39c'
