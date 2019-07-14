import re
import h5py
import numpy as np


def translate_output(directory, hdf_file, reactor_file):
    # Parse output Name
    file_name = reactor_file
    reactor_type = reactor_file[:-4]

    #Check to see if this is base model, or perturbed model
    if reactor_type[-4:] == '600K':
        try:
            hdf_file[reactor_type[:-5]].create_group(reactor_type)
        except KeyError:
            hdf_file.create_group(reactor_type[-5:])
            hdf_file[reactor_type[:-5]].create_group(reactor_type)
    elif reactor_type[-4:] in ['void', 'Void']:
        try:
            hdf_file[reactor_type[:-5]].create_group(reactor_type)
        except KeyError:
            hdf_file.create_group(reactor_type[-5:])
            hdf_file[reactor_type[:-5]].create_group(reactor_type)
    else:
        try:
            hdf_file[reactor_type].create_group(reactor_type)
        except KeyError:
            hdf_file.create_group(reactor_type)
            hdf_file[reactor_type].create_group(reactor_type)

    try:
        base_reactor = hdf_file[reactor_type]
    except KeyError:
        base_reactor = hdf_file[reactor_type[:-5]]

    reactor = base_reactor[reactor_type]
    name_list = file_name.split('_')
    name_list.pop(0)
    name_list[-1] = name_list[-1].split('.')[0]

    condition = '900K'
    enrichment = '15Pu12U10Zr'

    for parameter in name_list:
        if parameter[0] == 'F':
            fuel_smear = float(parameter[2:])
        elif parameter[0] == 'H':
            fuel_height = float(parameter[1:])
        elif 'U' in parameter:
            enrichment = parameter
        else:
            condition = parameter

    init_attr = {'smear': fuel_smear, 'height': fuel_height, 'enrichment': np.string_(enrichment), 'condition': np.string_(condition)}

    for k, v in init_attr.items():
        reactor.attrs.create(k, v)

    reactor.attrs['condition'] = condition
    attributes = {}
    # Read the file and extract the information
    file_path = directory +'\\' + file_name

    with open(file_path, 'rt') as file:
        for line in file:
            #add keff and uncertainty
            if line[0:16] == ' | the final est':
                val = re.findall(r'\d.\d\d\d\d\d', line)
                attributes['keff'] = float(val[0])
                attributes['keff_unc'] = float(val[1])
            #add thermal, epithermal, and fast fractions
            elif line[0:22] == ' |         (<0.625 ev)':
                val = re.findall(r'[\s\d]\d.\d\d', line)
                attributes['thermal_fraction'] = float(val[0])
                attributes['epithermal_fraction'] = float(val[1])
                attributes['fast_fraction'] = float(val[2])
            #add average number of neutrons gen per fission
            elif line[0:21] == ' | the average number':
                val = re.findall(r'\d.\d\d\d', line)
                attributes['nu-bar'] = float(val[0])
            # add escape, capture, and fission fractions
            elif line[0:20] == '            fraction':
                val = re.findall(r'\d.\d\d\d\d\dE-\d\d', line)
                attributes['escape_fraction'] = float(val[0])
                attributes['capture_fraction'] = float(val[1])
                attributes['fission_fraction'] = float(val[2])
            #add generation time and uncertainty
            elif line[0:20] == '           gen. time':
                # Excessively large generation times will be in micro-seconds not nano-seconds
                # Grab nano-second values
                try:
                    val = re.findall(r'[\s\d]\d\d.\d\d\d\d\d', line)
                    attributes['gen_time'] = float(val[0])
                    val = re.findall(r'[\s\d]\d.\d\d\d\d\d', line)
                    attributes['gen_time_unc'] = float(val[0])
                # Grab mico-second values and convert to nano-seconds
                except IndexError:
                    val = re.findall(r'[\s\d]\d.\d\d\d\d\d', line)
                    attributes['gen_time'] = float(val[0])*1000
                    val = re.findall(r'[\s\d]\d.\d\d\d\d\d', line)
                    attributes['gen_time_unc'] = float(val[0])*1000
            #add rossi-alpha and uncertainty
            elif line[0:20] == '         rossi-alpha':
                # Excessively large alpha-rossi values will be in micro-seconds not nano-seconds
                # Grab nano-second values
                if line[-8:-1] == '(/usec)':
                    val = re.findall(r'[-\s]\d.\d\d\d\d\dE-\d\d', line)
                    attributes['rossi_alpha'] = float(val[0])*1000
                    attributes['rossi_alpha_unc'] = float(val[1])*1000
                else:
                    val = re.findall(r'[-\s]\d.\d\d\d\d\dE-\d\d', line)
                    attributes['rossi_alpha'] = float(val[0])
                    attributes['rossi_alpha_unc'] = float(val[1])

            #add beta-eff and uncertainty
            elif line[0:20] == '            beta-eff':
                val = re.findall(r'\d.\d\d\d\d\d', line)
                attributes['beta'] = float(val[0])
                attributes['beta_unc'] = float(val[1])
    for k, v in attributes.items():
        reactor.attrs.create(k, v)

#translate_output('FC_FS76_H65.out', 'blank')