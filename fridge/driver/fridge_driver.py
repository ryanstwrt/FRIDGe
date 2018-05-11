from FRIDGe.fridge.input_readers import geometry_reader as geo_read
from FRIDGe.fridge.driver import assembly_holder as ah
from FRIDGe.fridge.driver import assembly_maker

print('Welcome to FRIDGe, the Fast Reactor Input Deck Generator!')
assembly_type = 'A271'# input('Please input the assembly type you would like to model: ')

fuel, assembly, plenum, fuel_reflector = geo_read.fuel_assembly_geometry_reader(assembly_type)

fuel_assembly = ah.Assembly(assembly, plenum, fuel_reflector, fuel, 100)
assembly_maker.assembly_maker(fuel_assembly)
print(fuel_assembly.universe_mcnp_surface)
file = open("test_case", "w")
file.write(fuel_assembly.pin.fuel_pellet_mcnp_cell + fuel_assembly.pin.fuel_bond_mcnp_cell + fuel_assembly.pin.fuel_clad_mcnp_cell+
           fuel_assembly.pin.fuel_universe_mcnp_cell+ fuel_assembly.pin.na_mcnp_cell+ fuel_assembly.lower_reflector_mcnp_cell+
           fuel_assembly.plenum_mcnp_cell+ fuel_assembly.upper_reflector_mcnp_cell+ fuel_assembly.lattice_mcnp_cell+
           fuel_assembly.lattice_holder_mcnp_cell+ fuel_assembly.void_mcnp_cell)
file.write("\nc Surface Cards\n")
file.write(fuel_assembly.pin.fuel_universe_mcnp_surface+ fuel_assembly.lower_reflector_mcnp_surface+ fuel_assembly.plenum_mcnp_surface+
           fuel_assembly.upper_reflector_mcnp_surface+ fuel_assembly.inner_duct_mcnp_surface+ fuel_assembly.outer_duct_mcnp_surface+
           fuel_assembly.pin.fuel_pellet_mcnp_surface + fuel_assembly.pin.fuel_bond_mcnp_surface + fuel_assembly.pin.fuel_clad_mcnp_surface +
           fuel_assembly.lower_plane_surface_mcnp+ fuel_assembly.upper_plane_surface_mcnp + fuel_assembly.universe_mcnp_surface)
file.close()
#print(fuel_assembly.lower_reflector_mcnp_surface)
#print(fuel_assembly.plenum_mcnp_surface)
#print(fuel_assembly.upper_reflector_mcnp_surface)
#print(fuel_assembly.inner_duct_mcnp_surface)
#print(fuel_assembly.universe_mcnp_surface)
print(fuel_assembly.pin.fuel_pellet_mcnp_surface)
print(fuel_assembly.pin.fuel_bond_mcnp_surface)
print(fuel_assembly.pin.fuel_clad_mcnp_surface)
print(fuel_assembly.pin.fuel_pin_universe_mcnp_surface)

print(fuel_assembly.pin.fuel_pellet_mcnp_cell)
print(fuel_assembly.pin.fuel_bond_mcnp_cell)
print(fuel_assembly.pin.fuel_clad_mcnp_cell)
print(fuel_assembly.pin.fuel_universe_mcnp_cell)
print(fuel_assembly.pin.na_mcnp_cell)
print(fuel_assembly.lower_reflector_mcnp_cell)
print(fuel_assembly.plenum_mcnp_cell)
print(fuel_assembly.upper_reflector_mcnp_cell)
print(fuel_assembly.lattice_mcnp_cell)
print(fuel_assembly.lattice_holder_mcnp_cell)
print(fuel_assembly.void_mcnp_cell)


