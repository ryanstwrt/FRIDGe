import fridge.driver.global_variables as gb
import os

def test_global_variables_default():
    """Check that the default variables are set correctly"""

    global_variables = gb.GlobalVariables()
    assert global_variables.assembly_file_name == ''
    assert global_variables.xc_set == ''
    assert global_variables.xc_library == ''
    assert global_variables.universe == 100
    assert global_variables.cellNumber == 100
    assert global_variables.surfaceNumber == 100
    assert global_variables.materialNumber == 100
    assert global_variables.temperature == 0
    assert global_variables.temp_adjusted_density is False
    assert global_variables.temp_adjusted_volume is False
    assert global_variables.clad_smear is False
    assert global_variables.bond_smear is False
    assert global_variables.void_per == 0
    assert global_variables.file_name == ''
    assert global_variables.number_generations == 0
    assert global_variables.number_skipped_generations == 0
    assert global_variables.number_particles_generation == 0
    assert global_variables.kopts is False
    assert global_variables.ksens is False
    assert global_variables.output_name == ''
    assert global_variables.input_type == ''


def test_global_variables_read_assembly():
    """Check the read_assembly function"""
    global_variables = gb.GlobalVariables()
    global_variables.read_input_file('A271_Assembly_Test')

    assert global_variables.assembly_file_name == 'A271_Assembly_Test'
    assert global_variables.xc_set == '.71c'
    assert global_variables.xc_library == 'ENDFVII.0'
    assert global_variables.universe == 100
    assert global_variables.cellNumber == 100
    assert global_variables.surfaceNumber == 100
    assert global_variables.materialNumber == 100
    assert global_variables.temperature == 600
    assert global_variables.temp_adjusted_density is True
    assert global_variables.temp_adjusted_volume is True
    assert global_variables.clad_smear is True
    assert global_variables.bond_smear is True
    assert global_variables.file_name == 'A271_Test'
    assert global_variables.number_generations == 2300
    assert global_variables.number_skipped_generations == 300
    assert global_variables.number_particles_generation == 1e10
    assert global_variables.kopts is True
    assert global_variables.ksens is True
    assert global_variables.output_name == 'Fuel_Assembly_Test'
    assert global_variables.input_type == 'Single'

def test_global_variables_read_core_burnup():
    """Check the read_assembly function"""
    global_variables = gb.GlobalVariables()
    global_variables.read_input_file('Full_Core_Test_Burnup')

    assert global_variables.assembly_file_name == 'Full_Core_Test_Burnup'
    assert global_variables.xc_set == '.37c'
    assert global_variables.xc_library == 'JEFF3.1'
    assert global_variables.temperature == 900
    assert global_variables.file_name == 'Core_Test'
    assert global_variables.number_generations == 230
    assert global_variables.number_skipped_generations == 30
    assert global_variables.number_particles_generation == 1e3
    assert global_variables.kopts is True
    assert global_variables.output_name == 'Full_Core_Test_Burnup'
    assert global_variables.input_type == 'Core'
    assert global_variables.burnup is True
    assert global_variables.power == 100
    assert global_variables.burnup_time == [50,100,150]
    assert global_variables.power_fraction == [1.0,1.0,1.0]


def test_global_variables_read_core_bad_burnup():
    """Check the read_assembly function"""
    global_variables = gb.GlobalVariables()
    global_variables.read_input_file('Full_Core_Test_Bad_Burnup')

    assert global_variables.assembly_file_name == 'Full_Core_Test_Bad_Burnup'
    assert global_variables.xc_set == '.73c'
    assert global_variables.xc_library == 'ENDFVII.0'
    assert global_variables.temperature == 1200
    assert global_variables.file_name == 'Core_Test'
    assert global_variables.number_generations == 230
    assert global_variables.number_skipped_generations == 30
    assert global_variables.number_particles_generation == 1e3
    assert global_variables.kopts is True
    assert global_variables.output_name == 'Full_Core_Test_Bad_Burnup'
    assert global_variables.input_type == 'Core'
    assert global_variables.burnup is True
    assert global_variables.power == 100
    assert global_variables.burnup_time == [50,100,150]
    assert global_variables.power_fraction == []