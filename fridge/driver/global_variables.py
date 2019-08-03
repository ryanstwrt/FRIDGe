import os
import glob
import yaml


class GlobalVariables(object):
    """
    This class will hold all the variables that are not specific to a single assembly.
    """
    def __init__(self):
        self.assembly_file_name = ''
        self.xc_library = ''
        self.xc_set = ''
        self.universe = 100
        self.cellNumber = 100
        self.surfaceNumber = 100
        self.materialNumber = 100
        self.temperature = 0
        self.temp_adjusted_density = False
        self.temp_adjusted_volume = False
        self.clad_smear = False
        self.bond_smear = False
        self.void_per = 0
        self.file_name = ''
        self.number_generations = 0
        self.number_skipped_generations = 0
        self.number_particles_generation = 0
        self.kopts = False
        self.ksens = False
        self.assembly_perturbations = {}
        self.output_name = ''
        self.input_type = ''

    def read_input_file(self, assembly_name, **perturbations):
        """Reads the yaml file for a FRIDGE input file and assigns any variables found."""
        self.assembly_file_name = assembly_name
        cur_dir = os.path.dirname(__file__)
        input_dir = os.path.join(cur_dir, "../fridge_input_file")
        assembly_path = os.path.join(input_dir, self.assembly_file_name + '.yaml')
        assembly_file = glob.glob(assembly_path)
        print(assembly_name, assembly_file)
        print(assembly_path)
        with open(assembly_file[0], "r") as file:
            inputs = yaml.safe_load(file)

        self.file_name = inputs["Name"]
        self.input_type = inputs["Input Type"]
        self.output_name = inputs["Output File Name"] \
            if "Output File Name" in inputs else 'FRIDGe1'
        self.temperature = float(inputs["Temperature"]) \
            if 'Temperature' in inputs else 900
        self.temp_adjusted_density = bool(inputs["Temperature Adjusted Density"]) \
            if 'Temperature Adjusted Density' in inputs else False
        self.temp_adjusted_volume = bool(inputs["Temperature Adjusted Volume"]) \
            if 'Temperature Adjusted Volume' in inputs else False
        self.clad_smear = bool(inputs["Smear Clad"]) \
            if 'Smear Clad' in inputs else False
        self.bond_smear = bool(inputs["Smear Bond"]) \
            if 'Smear Bond' in inputs else False
        self.xc_library = inputs["XC Library"] \
            if 'XC Library' in inputs else ''
        self.number_generations = int(inputs["Number of Generations"]) \
            if 'Number of Generations' in inputs else 230
        self.number_skipped_generations = int(inputs["Number of Skipped Generations"]) \
            if 'Number of Skipped Generations' in inputs else 30
        self.number_particles_generation = int(float(inputs["Number of Particles per Generation"])) \
            if 'Number of Particles per Generation' in inputs else int(1e6)
        self.kopts = bool(inputs["Run Kinetics"]) \
            if 'Run Kinetics' in inputs else False
        self.ksens = bool(inputs["ksens"]) \
            if 'ksens' in inputs else False
        self.void_per = float(inputs["Void Percent"]) \
            if "Void Percent" in inputs else 1.0
        self.assembly_perturbations = inputs["Assembly Perturbations"] \
            if "Assembly Perturbations" in inputs else {}

        # Update for perturbations
        for k, v in perturbations.items():
            self.__setattr__(k, v)

        # Set the XC set depending on the temperature
        if self.temperature == 600:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.81c'
            elif self.xc_library == 'ENDFVII.0':
                self.xc_set = '.71c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.34c'
        elif self.temperature == 900:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.82c'
            elif self.xc_library == 'ENDFVII.0':
                self.xc_set = '.72c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.37c'
        elif self.temperature == 1200:
            if self.xc_library == 'ENDFVII.1':
                self.xc_set = '.83c'
            elif self.xc_library == 'ENDFVII.0':
                self.xc_set = '.73c'
            elif self.xc_library == 'JEFF3.1':
                self.xc_set = '.39c'

    def update_numbering(self):
        self.universe += 20
        self.cellNumber += 20
        self.surfaceNumber += 20
        self.materialNumber += 20
