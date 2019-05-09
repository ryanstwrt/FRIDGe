import fridge.driver.reactorMaker as rM
import fridge.driver.global_variables as gb
import filecmp
import os
import glob

global_vars = gb.GlobalVariables()
cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, '../mcnp_input_files/')


def test_singleAssembly_Fuel():
    global_vars.read_input_file('A271_Assembly_Test')
    rM.single_assembly_maker(global_vars)
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Fuel_Assembly_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Fuel_Assembly_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True


def test_singleAssembly_Blank():
    global_vars.read_input_file('Blank_Assembly_Test')
    rM.single_assembly_maker(global_vars)
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Blank_Assembly_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Blank_Assembly_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True


def test_fullCore():
    global_vars.read_input_file('Full_Core_Test')
    rM.core_maker(global_vars)
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True


def test_fullCore_void():
    global_vars.read_input_file('Full_Core_Void_Test')
    rM.core_maker(global_vars)
    knownTestFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Void_Test.i'))
    testFile = glob.glob(os.path.join(mcnp_dir, 'Prefab_Full_Core_Void_Test.i'))
    assert filecmp.cmp(testFile[0], knownTestFile[0]) is True