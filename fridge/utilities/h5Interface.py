import h5py
import numpy as np
import fridge.utilities.outputInterface as OI
import os

class h5Interface(object):
    
    def __init__(self, output_name='test'):
        self.mcnp_file_name = None
        self.core_name = None
        self.params = None
        self.h5File = None
        self.outputInterface = None
        self.assembly_ind_vars = None
        self.dt_str = h5py.string_dtype(encoding='utf-8')
    
    def create_h5(self, file_name, path=None):
        """Create an H5 datafile from an outputInterface class"""
        self.mcnp_file_name = file_name
        self.params = file_name.split('_')[1:]
        self.core_name = '_'.join(self.params)
        self.h5file = h5py.File(self.core_name + '.h5', 'w')
        self.get_reactor_ind_vars()
        
        bu = True if self.assembly_ind_vars['condition'] == b'BU' else False
        self.outputInterface = OI.OutputReader('{}{}.out'.format(path,self.mcnp_file_name), burnup=bu)
        self.outputInterface.read_input_file()
        
        self.h5file.create_group(self.core_name)
        self.h5file[self.core_name].create_group('independent variables')
        for k,v in self.assembly_ind_vars.items():
            self.h5file[self.core_name]['independent variables'][k] = [v]
            
        for step, params in  self.outputInterface.cycle_dict.items():
            self.h5file[self.core_name].create_group(step)
            self.h5file[self.core_name][step].create_group('rx_parameters')
            self.h5file[self.core_name][step].create_group('assemblies')
            for k, v in params.items():
                if k == 'rx_parameters':
                    self.convert_rx_parameters(v, step)
                elif k == 'assemblies':
                    self.convert_assembly_parameters(v, step)

    def convert_assembly_parameters(self, params, step):
        """Write the assembly paramaters for each time step in a burnup
        TODO: Find a way to incorporate attributes"""
        core_group = self.h5file[self.core_name][step]['assemblies']
        for k,v in params.items():
            str_a = str(k)
            core_group.create_group(str_a)
            for assem_param, val in v.items():
                if assem_param == 'actinide inventory':
                    core_group[str_a].create_group(assem_param)
                    for num, nuclide in enumerate(val.index):
                        core_group[str_a][assem_param][str(nuclide)] = val.iloc[num]
                else:
                    core_group[str_a][assem_param] = [val]
                    
    def convert_rx_parameters(self, params, step):
        """Write the reactor parameters for each step."""
        core_group = self.h5file[self.core_name][step]['rx_parameters']
        for k,v in params.items():
            if 'precursor' in k:
                core_group.create_group(k)
                for pre, val in v[step].items():
                    if type(val) == str: #skip the units, this will be removed from output
                        pass
                    else:
                        core_group[k][pre] = [val]
                                                 
            else: 
                core_group[k] = [v[0]]
        
    def read_h5(self):
        """Read an H5 file and create an outputInterface class"""
        pass
    
    def get_reactor_ind_vars(self):
        """Baed on the file name, glean information on the core design"""
        for params in self.params:
            if 'FS' in params:
                smear = float(params[2:])
            elif 'H' in params:
                height = float(params[1:])
            elif 'Zr' in params:
                try:
                    pu_content = float(params[:2])
                except KeyError:
                    pu_content = float(params[:1])
                u_content = 27.0 - pu_content
            else:
                condition = params
        self.assembly_ind_vars = {'smear': smear,
                                'height': height,
                                'pu_content': pu_content,
                                'u_content': u_content,
                                'condition': np.string_(condition)}