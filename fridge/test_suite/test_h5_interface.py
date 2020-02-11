import fridge.utilities.outputInterface as OI
import fridge.utilities.h5Interface as h5I
import h5py

def test_init():
    I = h5I.h5Interface()
    assert I.file_name == None
    assert I.h5File == None
    assert I.dt_str == h5py.string_dtype(encoding='utf-8')

def test_create_h5():
    I = h5I.h5Interface()
    I.create_h5('test_file')    
    assert I.file_name == 'test_file'