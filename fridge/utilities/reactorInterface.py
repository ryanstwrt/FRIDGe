class reactorInterface(object):
    """The reactor interface is an easy way to explore different parameters within a specific reactor.
    This includes multiple methods to query the database."""
    def __init__(self, reactor):
        self.rx = reactor
        self.rx_name = self.rx.name.split('/')[-1]
        self.init_burnup()
        self.assemblies = {}
        self.rx_step_params = {}
        self.rx_base = {}
        self.rx_void = {}
        self.rx_temp = {}
        
        self.init_base()
        self.init_void()
        self.init_temp()
        self.init_burnup()
                        
    def init_base(self):
        """Initialize the base core"""
        try:
            self.rx_base = self.rx[self.rx_name]['step_0']['rx_parameters']
        except KeyError:
            print("Warning: Core {} does not have a base core.".format(self.rx_name))

    def init_void(self):
        """Initialize the voided core"""
        try:
            self.rx_void = self.rx['{}_Void'.format(self.rx_name)]['step_0']['rx_parameters']
        except KeyError:
            print("Warning: Core {} does not have a voided core.".format(self.rx_name))            

    def init_temp(self):
        """Initialize the 600K core"""
        try:
            self.rx_temp = self.rx['{}_600K'.format(self.rx_name)]['step_0']['rx_parameters']
        except KeyError:
            print("Warning: Core {} does not have a 600K core.".format(self.rx_name))            
            
    def init_burnup(self):
        """Initialize burnup core(s)"""
        try:
            self.assemblies = {}
            self.rx_step_params = {}
            for step in self.rx['{}_BU'.format(self.rx_name)].keys():
                self.rx_step_params[step] = self.rx['{}_BU'.format(self.rx_name)][step]['rx_parameters']
                self.assemblies[step] = self.rx['{}_BU'.format(self.rx_name)][step]['assemblies']
        except KeyError:
            print("Warning: Core {} does not have a burnup core. No assemblies are present".format(self.rx_name))
        
    def get_assembly_average(self, step, param):
        """Get the average parameter of an assembly based on the time step"""
        assem_tot = 0
        for num, assem in enumerate(self.assemblies[step].values()):
            assem_val = assem[param][0]
            assem_tot += assem_val
        return assem_tot / num
    
    def get_assembly_min(self, step, param):
        """Get the max parameter of an assembly based on the time step"""
        assem_min = 1E100
        for name, assem in self.assemblies[step].items():
            if assem[param][0] < assem_min:
                assem_min = assem[param][0]
                assem_name = name
        return (assem_name, assem_min)

    def get_assembly_max(self, step, param):
        """Get the max parameter of an assembly based on the time step"""
        assem_min = 0.0
        for name, assem in self.assemblies[step].items():
            if assem[param][0] > assem_min:
                assem_min = assem[param][0]
                assem_name = name
        return (assem_name, assem_min)
    
    def get_peak_to_average(self, step, param):
        """Get the peak to average value for a core"""
        avg = self.get_assembly_average(step, param)
        peak_assem, peak_val = self.get_assembly_max(step, param)
        return (peak_assem, peak_val / avg)
    
    def get_assem_to_avg(self, step, param, assem):
        """Get the assembly to average value for the a specific assembly"""
        avg = self.get_assembly_average(step, param)
        return self.assemblies[step][assem] / avg
        
    def get_reactivity_swing(self, step_init, step_final):
        """Get the reactivity swing (in pcm) between two time steps"""
        keff_init = self.rx_step_params[step_init]['keff'][0]
        keff_final = self.rx_step_params[step_final]['keff'][0]
        return (keff_init - keff_final)/(keff_final*keff_init) * 1E5
    
    def get_doppler_coefficient(self):
        """Calculate the Doppler Coefficient for the reactor"""
        keff_low = self.rx_temp['keff'][0]
        keff_high = self.rx_base['keff'][0]
        doppler = (keff_high - keff_low) / (keff_high*keff_low*300) * 1E5
        return doppler
    
    def get_void_coefficient(self):
        """Calculate the void coefficient"""
        keff_base = self.rx_base['keff'][0]
        keff_void = self.rx_void['keff'][0]
        void = (keff_void - keff_base) / (keff_void*keff_base*99.99) *1E5
        return void