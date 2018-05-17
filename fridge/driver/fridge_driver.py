from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker
from FRIDGe.fridge.utilities import mcnp_input_deck_maker as midm

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
assembly_type = 'A271'# input('Please input the assembly type you would like to model: ')

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 100)
assembly_maker.assembly_maker(assembly)

midm.mcnp_input_deck_maker(assembly)
