import re
import numpy as np
import pandas as pd
from collections import OrderedDict

class OutputReader(object):
    """
    This class reads in an mcnp output file and parses the appropriate data
    """
    
    def __init__(self, f):
        """Initialize the OutputReader with the file name, and read in the file"""
        self.file_path = f
        try:
            file = open(f, 'r')
        except FileNotFoundError:
            print("Error: File {} does not exist. Enter a valid path name".format(f))
            exit()
        split_f = f.split('/')[-1]
        self.core_name = split_f.split('.')[0]
        self.output = file.readlines()
        file.close()
        
        self.burnup = False
        self.cycles = 0
        self.cycle_dict = {}
        self.assemblies_dict = OrderedDict()
        
        
    def get_global_parameters(self):
        "Get the global parameters for a specific cycle"
        current_cycle = 0
        correct_area = True
        for line_num, line in enumerate(self.output):
            if 'Correcter' in line:
                correct_area = True
            elif 'Predictor' in line:
                correct_area = False
            if 'keff = ' in line and correct_area:
                self.cycle_dict['step_{}'.format(current_cycle)] = {}
                self.scrap_rx_params(self.output[line_num:line_num+83], current_cycle)
                current_cycle += 1
        self.convert_rx_params()

    def get_assembly_parameters(self):
        """Get the assembly specific parametsr (burnup, power fraction, actinide inventory)"""
        self.cycles = len(self.cycle_dict)
        self.cycle_dict['assemblies'] = self.assemblies_dict
        correct_area = False
        for line_num, line in enumerate(self.output):
            if 'Individual Material Burnup' in line:
                correct_area = True
            if 'Material #: ' in line and correct_area:
                self.scrap_assembly_power(self.output[line_num:line_num+4+self.cycles])
            elif 'print table 220' in line: #Break before we get to summed materials
                break
            elif 'nuclide data' in line:
                self.scrap_assembly_nuclide_data(self.output[line_num:line_num+self.cycles*60]) #This is a bit sloppy as it will run into the nonactide inventory data, a better method could be implemented later.
                    
    def scrap_assembly_power(self, line_list):
        temp_dict = {}
        material = int(line_list[0].split(' ')[3])
        temp_dict['material'] = material
        power_dict = {}
        for time_step in range(self.cycles):
            power = {'duration': float(line_list[4+time_step].split('  ')[2]),
                     'time': float(line_list[4+time_step].split('  ')[3]),
                     'power fraction': float(line_list[4+time_step].split('  ')[5]),
                     'burnup': float(line_list[4+time_step].split('  ')[8]),}
            self.cycle_dict['step_{}'.format(time_step)]['assemblies'][material] = power           

    def scrap_assembly_nuclide_data(self, line_list):
        temp_dict = {}
        actinides = False
        for line_num, line in enumerate(line_list):
            if 'nuclide data' in line:
                material = int(line.split(' ')[10])
            if 'actinide inventory' in line:
                actinides = True
                zaid_dict = {}
                if int(line.split(' ')[5]) != material:
                    print('Warning: Material in nuclide inventory ({}) does not match material from nuclide data ({}). Check to ensure the output file has not been altered in any way.'.format(int(line.split(' ')[5]), material))
                time_step = int(line.split(' ')[11][:-1]) #-1 drops the comma after step #,
            if 'nonactinide inventory' in line:
                actinides = False
            if actinides:
                try:
                    zaid = int(line.split('  ')[2])
                    mass = float(line.split('  ')[3])
                    if mass > 0.0:
                        zaid_dict[zaid] = {'mass': mass,
                                           'activity': float(line.split('  ')[4]),
                                           'specific activity': float(line.split('  ')[5]),
                                           'atom density': float(line.split('  ')[6]),
                                           'atom fraction': float(line.split('  ')[7]),
                                           'mass fraction': float(line.split('  ')[8])}
                        self.cycle_dict['step_{}'.format(time_step)]['assemblies'][material]['actinide inventory'] = zaid_dict
                except:
                    pass
        
    def convert_rx_params(self):
        """Convert reactor parameters from dictionary to pandas dataframe"""
        
        df = pd.DataFrame()
        for cycle, rx_params in self.cycle_dict.items():
            params = rx_params['rx_parameters'] 
            temp_db = pd.DataFrame.from_dict(params, orient='index')
            temp_db.T
            self.cycle_dict[cycle]['rx_parameters'] = temp_db.T
        
        
    def scrap_rx_params(self, line_list, time_step):
        "Grab all of the global reactor parameters assocaited with an specific time step"
        temp_dict = {}
        temp_dict[time_step] = {}
        time_dict = temp_dict[time_step]
        keff = (float(line_list[0].split(' ')[9]), 
                float(line_list[0].split(' ')[-4]))
        time_dict['keff'] = keff[0]
        time_dict['keff_unc'] = keff[1]

        prompt_rmvl = (float(line_list[4].split(' ')[10]),
                       float(line_list[4].split(' ')[-2]), 
                       line_list[4].split(' ')[11])
        time_dict['prompt_removal_lifetime'] = prompt_rmvl
        
        avg_n_lethargy_energy_fission = (float(line_list[6].split(' ')[9]), 
                                         line_list[6].split(' ')[10], 
                                         float(line_list[7].split(' ')[13]), 
                                         line_list[7].split(' ')[14])
        time_dict['avg_n_lethargy_fission'] = (avg_n_lethargy_energy_fission[0], avg_n_lethargy_energy_fission[1])
        time_dict['avg_n_energy_fission'] = (avg_n_lethargy_energy_fission[2], avg_n_lethargy_energy_fission[3])
        
        fission_energy_fractions = (float(line_list[10].split('%')[0][-5:]),
                                    float(line_list[10].split('%')[1][-5:]),
                                    float(line_list[10].split('%')[2][-5:]))
        time_dict['thermal_fission_frac'] = fission_energy_fractions[0]
        time_dict['epithermal_fission_frac'] = fission_energy_fractions[1]
        time_dict['fast_fission_frac'] = fission_energy_fractions[2]
        
        avg_n_per_absorption_fission = (float(line_list[12].split('=')[1][:13]),
                                        float(line_list[13].split('=')[1][:13]),
                                        float(line_list[15].split('=')[1][:6]))
        time_dict['avg_n_gen_per_abs_fission'] = avg_n_per_absorption_fission[0]
        time_dict['avg_n_gen_per_abs_all'] = avg_n_per_absorption_fission[1]
        time_dict['avg_n_gen_per_fission'] = avg_n_per_absorption_fission[2]
        
        prompt_lifespan_fraction = (float(line_list[59].split('   ')[5]),
                                      float(line_list[59].split('   ')[6]),
                                      float(line_list[59].split('   ')[7]),
                                      float(line_list[59].split('   ')[8]),
                                     float(line_list[60].split('   ')[5]),
                                      float(line_list[60].split('   ')[6]),
                                      float(line_list[60].split('   ')[7]),
                                      float(line_list[60].split('   ')[8]))
        time_dict['lifespan_esc'] = prompt_lifespan_fraction[0]
        time_dict['lifespan_capt'] = prompt_lifespan_fraction[1]
        time_dict['lifespan_fission'] = prompt_lifespan_fraction[2]
        time_dict['lifespan_rem'] = prompt_lifespan_fraction[3]
        time_dict['frac_esc'] = prompt_lifespan_fraction[4]
        time_dict['frac_capt'] = prompt_lifespan_fraction[5]
        time_dict['frac_fission'] = prompt_lifespan_fraction[6]
        time_dict['frac_rem'] = prompt_lifespan_fraction[7]
        
        gen_time = (float(line_list[68].split('   ')[5]),
                     float(line_list[68].split('   ')[7]),
                     line_list[68].split('   ')[8])
        time_dict['generation_time'] = gen_time
        
        rossi_alpha = (float(line_list[69].split('   ')[4]),
                      float(line_list[69].split('   ')[5]),
                      line_list[69].split('   ')[6])
        time_dict['rossi-alpha'] = rossi_alpha
        
        beta = (float(line_list[70].split('   ')[7]),
                float(line_list[70].split('   ')[9]))
        time_dict['beta'] = beta
        
        
        precursor = {}
        for num, line in enumerate(line_list[77:83]):
            precursor[num+1] = ({'beta-eff': float(line.split('     ')[3]),
                                 'beta-eff_unc': float(line.split('     ')[4]),
                                 'energy': float(line.split('     ')[5]),
                                 'energy_unc': float(line.split('     ')[6]),
                                 'energy_units': 'MeV',
                                 'lambda-i': float(line.split('     ')[7]),
                                 'lambda-i_unc': float(line.split('     ')[8]),
                                 'lambda-i_units': '(/sec)',
                                 'half-life': float(line.split('     ')[9]),
                                 'half-life_units': '(sec)'})
        time_dict['precursors'] = precursor

        self.cycle_dict['step_{}'.format(time_step)]['rx_parameters'] = time_dict
                
        

        