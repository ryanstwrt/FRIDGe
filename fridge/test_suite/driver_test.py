import fridge.driver.fridge_driver as fd
import glob
import os
import filecmp

cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, '../mcnp_input_files/')


def test_fridge_driver_singleAssembly():
    """Test that the new files gets made to the right directory"""
    fd.main('A271_Assembly_Test')
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Fuel_Assembly_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Fuel_Assembly_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True


def test_fridge_driver_core():
    """Test that the new files gets made to the right directory"""
    fd.main('Full_Core_Test')
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True