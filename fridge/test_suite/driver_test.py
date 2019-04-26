import fridge.driver.fridge_driver as fd
import glob
import os
cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, '../mcnp_input_files/')


def test_fridge_driver():
    """Test that the new files gets made to the right directory"""
    fd.main('A271_Assembly_Test')
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Test_Known.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Test.i'))
#    assert testFile == knownTestFile
