import fridge.driver.fridge_driver as fd
core_list = ['FullCore_FS65_H50', 'FullCore_FS65_H55', 'FullCore_FS65_H60', 'FullCore_FS65_H65', 'FullCore_FS65_H70',
             'FullCore_FS65_H75', 'FullCore_FS65_H80', ]

for core in core_list:
    print('Core:' + core)
    core_type =  core[9:]
    assem = 'A271_' + core_type
    fuel = '11Pu9U10Zr'
    file = 'FC_' + core_type + '_' + fuel
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, output_name=file)
    file='FC_' + core_type + '_' + fuel + '_600K'
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, temperature=600, output_name=file)
    file='FC_' + core_type + '_' + fuel + '_Void'
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, void_per=0.001, output_name=file)
    fuel = '13Pu10U10Zr'
    print('Core: ' + core + ' ' + fuel)
    file = 'FC_' + core_type + '_' + fuel
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, output_name=file)
    file='FC_' + core_type + '_' + fuel + '_600K'
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, temperature=600, output_name=file)
    file='FC_' + core_type + '_' + fuel + '_Void'
    fd.main(core, assembly_perturbations={assem: {'fuelMaterial': fuel}}, void_per=0.001, output_name=file)
