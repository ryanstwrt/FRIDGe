import fridge.utilities.h5Interface as h5I
import fridge.utilities.reactorInterface as rI
import os

h5_interface = h5I.h5Interface(output_name='test')
h5_interface.create_h5()
for root, dirs, files in os.walk('fridge/test_suite'):
    for file in files:
        if '.out' in file and 'checkpoint' not in file:
            try:
                h5_interface.add_reactor(file, path=root)  
            except ValueError:
                pass
rx = rI.reactorInterface(h5_interface.h5file['FS65_H75_23Pu4U10Zr'])

            
def test_init():
    assert rx.rx == h5_interface.h5file['FS65_H75_23Pu4U10Zr']
    assert rx.rx_name == 'FS65_H75_23Pu4U10Zr'
    for step, assem_step in zip(['step_0','step_1','step_2','step_3','step_4','step_5','step_6'], rx.assemblies.keys()):
        assert step == assem_step

def test_get_assem_avg():
    avg_pow = rx.get_assembly_average('step_6', 'power fraction')
    assert round(avg_pow, 6) == 0.012987
    avg_bu = rx.get_assembly_average('step_6', 'burnup')
    assert round(avg_bu, 6) == 38.055065

def test_get_assem_min():
    min_pow = rx.get_assembly_min('step_6', 'power fraction')
    assert min_pow == ('1322', 9.136E-3)
    min_pow_2 = rx.get_assembly_min('step_0', 'power fraction')
    assert min_pow_2 == ('1522', 8.716E-3)
    min_bu = rx.get_assembly_min('step_6', 'burnup')
    assert min_bu == ('1722', 2.612E1)
    
def test_get_assem_max():
    max_pow = rx.get_assembly_max('step_6', 'power fraction')
    assert max_pow == ('122', 1.684E-2)
    max_pow_2 = rx.get_assembly_max('step_0', 'power fraction')
    assert max_pow_2 == ('222', 1.767E-2)
    max_bu = rx.get_assembly_max('step_6', 'burnup')
    assert max_bu == ('222', 5.070E1)

def test_get_peak_to_avg():
    peak_power = rx.get_peak_to_average('step_6', 'power fraction')
    assert (peak_power[0], round(peak_power[1],4)) == ('122', round((0.01684/0.012987),4))
    peak_bu = rx.get_peak_to_average('step_6', 'burnup')
    assert (peak_bu[0], round(peak_bu[1],4)) == ('222', round((50.70/38.055),4))

def test_get_Reactivity_swing():
    rx_swing = rx.get_reactivity_swing('step_0', 'step_6')
    assert round(rx_swing,2) == 5376.02