import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.Assembly.BlankAssembly as BlankAssembly
import fridge.utilities.mcnpCreatorFunctions as mcnpCF
import fridge.Core.Core as Core


def single_assembly_maker(global_vars):
    assembly_info = [global_vars.file_name, '01A01', global_vars, None]
    assembly_type = Assembly.read_assembly_type(global_vars.file_name)
    assembly = None
    if assembly_type == 'Fuel':
        assembly = FuelAssembly.FuelAssembly(assembly_info)
    elif assembly_type == 'Blank':
        assembly = BlankAssembly.BlankAssembly(assembly_info)
    k_card = mcnpCF.make_mcnp_problem(global_vars)
    mcnpCF.mcnp_input_deck_maker(assembly, k_card, global_vars)


def core_maker(global_vars):
    core = Core.Core()
    core_dict = core.read_core_data(global_vars.file_name)
    core_dict.pop('Name')
    core_dict.pop('Vessel Thickness')
    core_dict.pop('Vessel Material')
    core_dict.pop('Coolant Material')
    for position, assembly_name in core_dict.items():
        print('Building assembly {} in position {}.'.format(assembly_name, position))
        assembly_info = [assembly_name, position, global_vars, core]
        assembly_type = Assembly.read_assembly_type(assembly_name)
        assembly = None
        if assembly_type == 'Fuel':
            assembly = FuelAssembly.FuelAssembly(assembly_info)
        elif assembly_type == 'Blank':
            assembly = BlankAssembly.BlankAssembly(assembly_info)
        core.assemblyList.append(assembly)
        global_vars.update_numbering()
    print('Building reactor core and coolant.')
    core.build_core(global_vars)
    print('Creating MCNP input file.')
    k_card = mcnpCF.make_mcnp_problem(global_vars)
    mcnpCF.mcnp_input_deck_maker_core(core, k_card, global_vars)
