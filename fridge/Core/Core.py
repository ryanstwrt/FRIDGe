import glob
import yaml
import os

cur_dir = os.path.dirname(__file__)
geo_dir = os.path.join(cur_dir, "../data/core")


class Core:
    """"core class will hold all of the assemblies present in the core."""

    def __init__(self):
        self.name = ''
        self.assemblyList = []
        self.excessCoolant = None
        self.vessel = None
        self.vesselThickness = 0

    def getCoreData(self, coreFile):
        coreYamlFile = glob.glob(os.path.join(geo_dir, coreFile + '.yaml'))
        with open(coreYamlFile[0], 'r') as coreFile:
            inputs = yaml.safe_load(coreFile)
            self.name = inputs['Name']
            self.vesselThickness = inputs['Vessel Thickness']
        return inputs
