import fridge.utilities.outputInterface as OI
import os

def test_init():
    print(os.getcwd())
    interface = OI.OutputReader(r'test_suite/test_interface.txt')
    assert interface.output == ['Test Interface\n', '\n', 'More Testing']
    assert interface.burnup == False
    assert interface.cycles == 0
    assert interface.cycle_dict == {}
    assert interface.core_name == 'test_interface'