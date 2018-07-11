from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker
from FRIDGe.fridge.driver import data_maker as dm
from FRIDGe.fridge.utilities import mcnp_input_deck_maker as midm
from FRIDGe.fridge.driver import global_variables as gb

# TODO implement sodium voiding
# TODO implement temperature adjusted density
# TODO implement temperature adjusted volume
# TODO implement cladding smear
# TODO implement bond smear
# TODO add material creator
# TODO add fuel smear
# TODO add element creator
# TODO add catch for clad greater than sodium universe
# TODO add catch for clad+wire wrap greater than sodium universe
# TODO add catch for fuel/bond greater than each other or clad
# TODO Allow user to input fuel diameter
# TODO allow user to input
# TODO Finish adding test
# TODO Add more documentation
# TODO create atom number check for smear
# TODO turn geometry files into yaml files
# TODO turn material files into yaml files
# TODO convert failure message to a better system

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
file_name = 'A271_Assembly' #input('Please input the file name you would like to model: ')

global_vars = gb.global_variables(file_name)

assembly = ah.FuelAssembly(global_vars, global_vars.assembly_type)
assembly_maker.assembly_maker(assembly)

k_card = dm.make_mcnp_problem(global_vars)

midm.mcnp_input_deck_maker(assembly, k_card, global_vars)
