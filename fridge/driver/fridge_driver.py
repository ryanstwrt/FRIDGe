from FRIDGe.fridge.driver import data_maker as dm
import FRIDGe.fridge.driver.Assembly as assembly
from FRIDGe.fridge.utilities import mcnp_input_deck_maker as midm
from FRIDGe.fridge.driver import global_variables as gb

# TODO implement sodium voiding
# TODO implement fuel radial expansion (density/volume change)
# TODO implement fuel axial expansion
# TODO implement coolant expansion
# TODO implement clad expansion
# TODO implement homogenization
# TODO add sensitivity parameter's to input
# TODO split XC to fuel, coolant, structure
# TODO add catch for clad greater than sodium universe
# TODO add catch for clad+wire wrap greater than sodium universe
# TODO add catch for fuel/bond greater than each other or clad
# TODO Allow user to input fuel diameter
# TODO Finish adding tests
# TODO Add more documentation
# TODO create atom number check for smear
# TODO convert failure message to Assert Error messages

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
file_name = 'A271_Assembly' #input('Please input the file name you would like to model: ')

global_vars = gb.GlobalVariables()
global_vars.read_input_file(file_name)

assembly = assembly.FuelAssembly([global_vars.assembly_type, '01A01', global_vars])

k_card = dm.make_mcnp_problem(global_vars)

midm.mcnp_input_deck_maker(assembly, k_card, global_vars)
