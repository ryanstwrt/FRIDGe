import fridge.driver.fridge_driver as fd


def create_core(core_list, assem_perts={}):
    """Wrapper around FRIDGe to create multiple cores concurrently"""

    for core in core_list:
        print('Core: ' + core)
        core_type = core[9:17]
        print(core_type)
        file = 'FC_' + core_type + '_' + fuel
        fd.main(core, assembly_perturbations=assem_perts, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_600K'
        fd.main(core, assembly_perturbations=assem_perts, temperature=600, output_name=file)
        file='FC_' + core_type + '_' + fuel + '_Void'
        fd.main(core, assembly_perturbations=assem_perts, void_per=0.001, output_name=file)


cores = ['FullCore_FS70_H60_15Pu_12U']#, 'FullCore_FS50_H60_15Pu_12U', 'FullCore_FS50_H70_15Pu_12U', 'FullCore_FS50_H80_15Pu_12U']
fuel = '20Pu7U10Zr'
assembly = 'A271_FS70_H60'
create_core(cores, assem_perts={assembly: {'fuelMaterial': fuel}})
