import h5py

class h5Interface(object):
    
    def __init__(self):
        self.core_name = None
        self.h5File = None
        self.outputInterface = None
        self.dt_str = h5py.string_dtype(encoding='utf-8')
    
    def create_h5(self, OI):
        """Create an H5 datafile from an outputInterface class"""
        self.outputInterface = OI
        
        
    def read_h5(self):
        """Read an H5 file and create an outputInterface class"""
        pass