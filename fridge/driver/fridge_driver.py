from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker
from FRIDGe.fridge.utilities import mcnp_input_deck_maker as midm

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
assembly_type = 'A271'# input('Please input the assembly type you would like to model: ')

universe_number = 100

assembly = ah.Assembly(assembly_type, universe_number)
assembly_maker.assembly_maker(assembly)

midm.mcnp_input_deck_maker(assembly)
