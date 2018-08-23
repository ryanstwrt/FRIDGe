def mcnp_input_deck_maker(assembly, k_card, global_vars):
    file = open("../mcnp_input_files/" + global_vars.output_name + ".i", "w")
    file.write("Input deck created by FRIDGe\n")
    file.write("c " + "Title".center(77, "*") + "\n")
    assembly_cell_title = "Cell Cards for Assembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_cell_title.center(77, "*") + " \n")
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.fuelUniverse, assembly.innerDuct, assembly.duct, assembly.plenum,
             assembly.upperReflector, assembly.lowerReflector]
    for cell in units:
        file.write(cell.cellCard + '\n')
    file.write("\n")
    assembly_surface_title = "Surface Cards for FuelAssembly: {}".format(assembly.assemblyPosition)
    file.write("c " + assembly_surface_title.center(77, "*") + "\n")
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.innerDuct, assembly.duct, assembly.plenum,
             assembly.upperReflector, assembly.lowerReflector]
    for surface in units:
        file.write(surface.surfaceCard + '\n')
    file.write("\n")
    assembly_data_title = "Data Cards"
    file.write("c " + assembly_data_title.center(77, "*") + "\n")
    assembly_kcode_title = "k-code Information"
    file.write("c " + assembly_kcode_title.center(77, "*") + "\n")
    file.write(k_card)
    file.write("c " + "Material Information".center(77, "*") + "\n")
    units = [assembly.fuel, assembly.bond, assembly.clad, assembly.coolant, assembly.blankCoolant,
             assembly.duct, assembly.plenum,
             assembly.upperReflector, assembly.lowerReflector]
    for material in units:
        file.write(material.materialCard)
    file.close()

