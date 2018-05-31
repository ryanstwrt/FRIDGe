from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker
from FRIDGe.fridge.driver import data_maker as dm
from FRIDGe.fridge.utilities import mcnp_input_deck_maker as midm
from FRIDGe.fridge.driver import global_variables as gb

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
file_name = 'A271_Assembly'# input('Please input the assembly type you would like to model: ')

global_vars = gb.global_variables(file_name)

assembly = ah.Assembly(global_vars.assembly_type, global_vars.universe, global_vars)
assembly_maker.assembly_maker(assembly)

k_card = dm.make_mcnp_problem(global_vars)

midm.mcnp_input_deck_maker(assembly, k_card)
