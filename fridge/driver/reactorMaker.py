import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.Assembly.BlankAssembly as BlankAssembly
import fridge.utilities.mcnpCreatorFunctions as mcf
import fridge.Core.Core as Core
import copy


def singleAssemblyMaker(global_vars):
    assemblyInfo = [global_vars.file_name, '01A01', global_vars, None]
    assemblyLocation = Assembly.getAssemblyLocation(global_vars.file_name)
    assemblyType = Assembly.assemblyTypeReader(assemblyLocation)
    assembly = None
    if assemblyType == 'Fuel':
        assembly = FuelAssembly.FuelAssembly(assemblyInfo)
    elif assemblyType == 'Blank':
        assembly = BlankAssembly.BlankAssembly(assemblyInfo)
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker(assembly, k_card, global_vars)


def coreMaker(global_vars):
    core = Core.Core()
    coreDict = core.getCoreData(global_vars.file_name)
    coreDict.pop('Name')
    coreDict.pop('Vessel Thickness')
    coreDict.pop('Vessel Material')
    coreDict.pop('Coolant Material')
    for position, assemblyType in coreDict.items():
        print('Building assembly {} in position {}.'.format(assemblyType, position))
        assemblyInfo = [assemblyType, position, global_vars, core]
        assemblyLocation = Assembly.getAssemblyLocation(assemblyType)
        assemblyType = Assembly.assemblyTypeReader(assemblyLocation)
        assembly = None
        if assemblyType == 'Fuel':
            assembly = FuelAssembly.FuelAssembly(assemblyInfo)
        elif assemblyType == 'Blank':
            assembly = BlankAssembly.BlankAssembly(assemblyInfo)
        core.assemblyList.append(assembly)
        global_vars.updateNumbering()
    print('Building reactor core and coolant.')
    core.getCore(global_vars)
    print('Creating MCNP input file.')
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker_core(core, k_card, global_vars)
