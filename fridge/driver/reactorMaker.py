import fridge.Assembly.FuelAssembly as FuelAssembly
import fridge.Assembly.Assembly as Assembly
import fridge.Assembly.BlankAssembly as BlankAssembly
import fridge.utilities.mcnpCreatorFunctions as mcf
import fridge.Core.Core as Core
import copy


def singleAssemblyMaker(global_vars):
    assemblyInfo = [global_vars.file_name, '01A01', global_vars]
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
    for position, assemblyType in coreDict.items():
        print(position, assemblyType)
        assemblyInfo = [assemblyType, position, global_vars]
        assemblyLocation = Assembly.getAssemblyLocation(assemblyType)
        assemblyType = Assembly.assemblyTypeReader(assemblyLocation)
        assembly = None
        if assemblyType == 'Fuel':
            assembly = FuelAssembly.FuelAssembly(assemblyInfo)
        elif assemblyType == 'Blank':
            assembly = BlankAssembly.BlankAssembly(assemblyInfo)
        core.assemblyList.append(copy.deepcopy(assembly))
        global_vars.updateNumbering()
    core.getCoreData(global_vars.file_name)
    core.getCore(global_vars)
    k_card = mcf.make_mcnp_problem(global_vars)
    mcf.mcnp_input_deck_maker_core(core, k_card, global_vars)
