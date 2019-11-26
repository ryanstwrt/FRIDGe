import fridge.driver.reactorMaker as rM
import fridge.driver.global_variables as gb
import filecmp
import os
import glob

cur_dir = os.path.dirname(__file__)
mcnp_dir = os.path.join(cur_dir, '../mcnp_input_files/')
mcnp_test_dir = os.path.join(cur_dir, '../mcnp_input_files/Test_Inputs/')


def test_single_assembly_fuel():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Six_Axial_Fuel_Assembly_Test')
    rM.single_assembly_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Six_Assembly_Test.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Six_Assembly_Test.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True


def test_single_assembly_smear():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Axial_Smear_Assembly_Test')
    rM.single_assembly_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Smear_Assembly_Test.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Smear_Assembly_Test.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True


def test_full_core():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Full_Core_Test')
    rM.core_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Full_Core_Test.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Full_Core_Test.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True


def test_full_core_burnup():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Full_Core_Test_Burnup')
    rM.core_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Full_Core_Test_Burnup.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Full_Core_Test_Burnup.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True


def test_full_core_void():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Full_Core_Void_Test')
    rM.core_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Full_Core_Void_Test.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Full_Core_Void_Test.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True


def test_perturbed_core():
    global_vars = gb.GlobalVariables()
    global_vars.read_input_file('Full_Core_Test', assembly_perturbations={'A271_Six_Axial_Test':
                                {'fuelMaterial': 'U10Zr'}},
                                output_name='Perturbed_Test',
                                temperature=600,
                                void_per=0.001)
    rM.core_maker(global_vars)
    known_file = glob.glob(os.path.join(mcnp_test_dir, 'Prefab_Perturbed_Test.i'))
    test_file = glob.glob(os.path.join(mcnp_dir, 'Perturbed_Test.i'))
    assert filecmp.cmp(test_file[0], known_file[0]) is True
