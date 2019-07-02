import glob
import os
import fridge.utilities.utilities as utilities

cur_dir = os.path.dirname(__file__)
assembly_directory = os.path.join(cur_dir, "../data/assembly")


class Assembly(object):
    """
    Holds all information required for modeling a basic assembly and van be inherited to make specific assembly type.

    Current types include:
    Fuel Assembly
    .82c Assembly
    """

    def __init__(self, assembly_information):
        self.assembly_file_name = assembly_information[0]
        self.assemblyPosition = assembly_information[1]
        self.globalVars = assembly_information[2]
        self.core = assembly_information[3]
        self.universe = self.globalVars.universe
        self.cellNum = self.globalVars.cellNumber
        self.surfaceNum = self.globalVars.surfaceNumber
        self.materialNum = self.globalVars.materialNumber
        self.xcSet = self.globalVars.xc_set
        self.voidPercent = self.globalVars.void_per
        self.assemblyType = ''
        self.assemblyType = ''
        self.pinsPerAssembly = 0
        self.assemblyPitch = 0.0
        self.ductInnerFlatToFlat = 0.0
        self.ductOuterFlatToFlat = 0.0
        self.ductOuterFlatToFlatMCNPEdge = 0.0
        self.assemblyHeight = 0.0
        self.zPosition = 0.0
        self.coolantMaterial = ''
        self.assemblyMaterial = ''
        self.zPosition = 0.0
        assembly_yaml_file = glob.glob(os.path.join(assembly_directory, self.assembly_file_name + '.yaml'))
        self.inputs = utilities.yaml_reader(assembly_yaml_file, assembly_directory, self.assembly_file_name)

    def get_assembly_data(self, inputs):
        """Assign assembly parameters based on the yaml Assembly file."""
        self.assemblyType = inputs['Assembly Type']
        self.pinsPerAssembly = int(inputs['Pins Per Assembly']) if 'Pins Per Assembly' in inputs else 0
        self.assemblyPitch = float(inputs['Assembly Pitch'])
        self.ductInnerFlatToFlat = float(inputs['Duct Inside Flat to Flat']) / 2 if 'Duct Inside Flat to Flat' in \
            inputs else 0.0
        thickness = float(inputs['Duct Thickness']) if 'Duct Thickness' in inputs else 0.0
        self.ductOuterFlatToFlat = self.ductInnerFlatToFlat + thickness
        self.ductOuterFlatToFlatMCNPEdge = self.ductOuterFlatToFlat * 1.00005
        self.assemblyHeight = float(inputs['Assembly Height'])
        if self.core is None:
            self.coolantMaterial = inputs['Coolant Material']
        else:
            self.coolantMaterial = self.core.coolantMaterial
        self.assemblyMaterial = inputs['Assembly Material']
        self.zPosition = float(inputs['Z Position']) if 'Z Position' in inputs else 0.0

    def update_global_identifiers(self, universe_test):
        """Updates cell, surface, material, and universe number to create uniqueness."""
        self.cellNum += 1
        self.surfaceNum += 1
        self.materialNum += 1
        if universe_test:
            self.universe += 1

    def update_perturbations(self):
        """Update the variables for any perturbations in the input file"""
        for a, perts in self.globalVars.assembly_perturbations.items():
            if a == self.assembly_file_name:
                for k, v in perts.items():
                    self.__setattr__(k, v)

def read_assembly_type(assembly_file_name):
    """Reads in the assembly type to determine what type of assembly to build and return it."""
    assembly_yaml_file = glob.glob(os.path.join(assembly_directory, assembly_file_name + '.yaml'))
    inputs = utilities.yaml_reader(assembly_yaml_file, assembly_directory, assembly_file_name)
    assembly_type = inputs['Assembly Type']
    return assembly_type
