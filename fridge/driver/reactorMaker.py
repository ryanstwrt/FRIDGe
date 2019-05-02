import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.Assembly.BlankAssembly as BlankAssembly
import fridge.utilities.mcnpCreatorFunctions as mcf
import fridge.Core.Core as Core


def singleAssemblyMaker(global_vars):
    assemblyInfo = [global_vars.file_name, '01A01', global_vars, None]
    assemblyType = Assembly.read_assembly_type(global_vars.file_name)
    assembly = None
    if assemblyType == 'Fuel':
        assembly = FuelAssembly.FuelAssembly(assemblyInfo)
    elif assemblyType == 'Blank':
        assembly = BlankAssembly.BlankAssembly(assemblyInfo)
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker(assembly, k_card, global_vars)


def coreMaker(global_vars):
    core = Core.Core()
    coreDict = core.read_core_data(global_vars.file_name)
    coreDict.pop('Name')
    coreDict.pop('Vessel Thickness')
    coreDict.pop('Vessel Material')
    coreDict.pop('Coolant Material')
    for position, assembly_name in coreDict.items():
        print('Building assembly {} in position {}.'.format(assembly_name, position))
        assembly_info = [assembly_name, position, global_vars, core]
        assemblyType = Assembly.read_assembly_type(assembly_name)
        assembly = None
        if assemblyType == 'Fuel':
            assembly = FuelAssembly.FuelAssembly(assembly_info)
        elif assemblyType == 'Blank':
            assembly = BlankAssembly.BlankAssembly(assembly_info)
        core.assemblyList.append(assembly)
        global_vars.updateNumbering()
    print('Building reactor core and coolant.')
    core.build_core(global_vars)
    print('Creating MCNP input file.')
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker_core(core, k_card, global_vars)
