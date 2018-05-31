def mcnp_input_deck_maker(assembly, k_card):
    file = open("../mcnp_input_files/test_case.i", "w")
    file.write("Input deck created by FRIDGe\n")
    file.write("c " + "Title".center(77, "*") + "\n")
    assembly_cell_title = "Cell Cards for FuelAssembly: " + str(assembly.assembly_universe)
    file.write("c " + assembly_cell_title.center(77, "*") + " \n")
    file.write(assembly.pin.fuel_pellet_mcnp_cell +
               assembly.pin.fuel_bond_mcnp_cell +
               assembly.pin.fuel_clad_mcnp_cell +
               assembly.pin.fuel_universe_mcnp_cell +
               assembly.pin.na_mcnp_cell +
               assembly.lower_reflector_mcnp_cell +
               assembly.plenum_mcnp_cell +
               assembly.upper_reflector_mcnp_cell +
               assembly.lattice_mcnp_cell +
               assembly.lattice_holder_mcnp_cell +
               assembly.void_mcnp_cell)
    file.write("\n")
    assembly_surface_title = "Surface Cards for FuelAssembly: " + str(assembly.assembly_universe)
    file.write("c " + assembly_surface_title.center(77, "*") + "\n")
    file.write(assembly.pin.fuel_universe_mcnp_surface +
               assembly.lower_reflector_mcnp_surface +
               assembly.plenum_mcnp_surface +
               assembly.upper_reflector_mcnp_surface +
               assembly.inner_duct_mcnp_surface +
               assembly.outer_duct_mcnp_surface +
               assembly.pin.fuel_pellet_mcnp_surface +
               assembly.pin.fuel_bond_mcnp_surface +
               assembly.pin.fuel_clad_mcnp_surface +
               assembly.pin.fuel_pin_universe_mcnp_surface +
               assembly.pin.na_cell_mcnp_surface +
               assembly.lower_plane_surface_mcnp +
               assembly.upper_plane_surface_mcnp +
               assembly.universe_mcnp_surface)
    file.write("\n")
    assembly_data_title = "Data Cards"
    file.write("c " + assembly_data_title.center(77, "*") + "\n")
    assembly_kcode_title = "k-code Information"
    file.write("c " + assembly_kcode_title.center(77, "*") + "\n")
    file.write(k_card)
    file.write("c " + "Material Information".center(77, "*") + "\n")
    file.write(assembly.material.fuel_mcnp_data +
               assembly.material.bond_mcnp_data +
               assembly.material.clad_mcnp_data +
               assembly.material.fuel_reflector_mcnp_data +
               assembly.material.plenum_mcnp_data +
               assembly.material.wire_wrap_smear_mcnp_data)
    file.close()
