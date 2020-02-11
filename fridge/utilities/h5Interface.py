import h5py

class h5Interface(object):
    
    def __init__(self):
        self.file_name = None
        self.h5File = None
        self.outputInterface = None
        self.dt_str = h5py.string_dtype(encoding='utf-8')
    
    def create_h5(self, file_name):
        """Create an H5 datafile from an outputInterface class"""
        self.file_name = file_name
        self.h5file = h5py.File(self.file_name + '.h5', 'w')
        

        
    def read_h5(self):
        """Read an H5 file and create an outputInterface class"""
        pass