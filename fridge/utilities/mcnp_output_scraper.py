import re
import h5py
import numpy as np


def translate_output(directory, hdf_file, reactor_file):
    dt = h5py.string_dtype(encoding='utf-8')
    # Parse output Name
    file_name = reactor_file
    reactor_type = reactor_file[:-4]
    # Check to see if this is base model, or perturbed model
    # This will also create the HDF group for the base model
    if reactor_type[-4:] == '600K':
        base_reactor = create_hdf_group(hdf_file, reactor_type, reactor_type[:-5])
    elif reactor_type[-4:] in ['void', 'Void']:
        base_reactor = create_hdf_group(hdf_file, reactor_type, reactor_type[:-5])
    else:
        base_reactor = create_hdf_group(hdf_file, reactor_type, reactor_type)

    #Prep the output file name for parsing and assigning
    reactor = base_reactor[reactor_type]
    name_list = file_name.split('_')
    name_list.pop(0)
    name_list[-1] = name_list[-1].split('.')[0]

    condition = '900K'
    enrichment = '15Pu12U10Zr'
    temperature = 900

    for parameter in name_list:
        # Find the fuel smear designated FSxx
        if parameter[0] == 'F':
            fuel_smear = float(parameter[2:])
        # Find the fuel height designate Hxx
        elif parameter[0] == 'H':
            fuel_height = float(parameter[1:])
        # Find the enrichment types designated xxUxxPu or xxPuxxU
        elif 'U' in parameter:
            enrichment = parameter
        # Find the condition of the reactor either 600K or void
        else:
            condition = parameter
            if 'K' in condition:
                temperature = float(condition[:-1])

    init_attr = {'smear': fuel_smear, 'height': fuel_height, 'enrichment': np.string_(enrichment),
                 'condition': np.string_(condition), 'temperature': temperature}

    for k, v in init_attr.items():
        if type(v) == np.bytes_:
            ds = reactor.create_dataset(k, (1,), dtype=dt)
        else:
            ds = reactor.create_dataset(k, (1,))
        ds[0] = v

    attributes = {}
    # Read the file and extract the information
    file_path = directory +'\\' + file_name

    with open(file_path, 'rt') as file:
        for line in file:
            #add keff and uncertainty
            if line[0:16] == ' | the final est':
                val = re.findall(r'\d.\d\d\d\d\d', line)
                attributes['keff'] = [float(val[0]), float(val[1])]
            #add thermal, epithermal, and fast fractions
            elif line[0:22] == ' |         (<0.625 ev)':
                val = re.findall(r'[\s\d]\d.\d\d', line)
                attributes['thermal_fraction'] = [float(val[0])]
                attributes['epithermal_fraction'] = [float(val[1])]
                attributes['fast_fraction'] = [float(val[2])]
            #add average number of neutrons gen per fission
            elif line[0:21] == ' | the average number':
                val = re.findall(r'\d.\d\d\d', line)
                attributes['nu-bar'] = [float(val[0])]
            # add escape, capture, and fission fractions
            elif line[0:20] == '            fraction':
                val = line.split('    ')
                attributes['escape_fraction'] = [float(val[4])]
                attributes['capture_fraction'] = [float(val[5])]
                attributes['fission_fraction'] = [float(val[6])]
            #add generation time and uncertainty
            elif line[0:20] == '           gen. time':
                # Excessively large generation times will be in micro-seconds not nano-seconds
                # Grab nano-second values
                val = line.split('    ')
                if 'usec' in val[-1]:
                    attributes['gen_time'] = [float(val[-4])*1000, float(val[-2])*1000]
                else:
                    attributes['gen_time'] = [float(val[-4]), float(val[-2])]
            #add rossi-alpha and uncertainty
            elif line[0:20] == '         rossi-alpha':
                # Excessively large alpha-rossi values will be in micro-seconds not nano-seconds
                # Grab nano-second values
                val = line.split('    ')
                if 'usec' in val[-1]:
                    attributes['gen_time'] = [float(val[-3])/1000, float(val[-2])/1000]
                else:
                    attributes['gen_time'] = [float(val[-3]), float(val[-2])]
            #add beta-eff and uncertainty
            elif line[0:20] == '            beta-eff':
                val = line.split('        ')
                attributes['beta'] = [float(val[-2]), float(val[-1])]

    for k, v in attributes.items():
        ds = reactor.create_dataset(k, (len(v),))
        for l in range(len(v)):
            ds[l] = v[l]

def create_hdf_group(hdf_file, specific, general):
    try:
        hdf_file[general].create_group(specific)
    except KeyError:
        hdf_file.create_group(general)
        hdf_file[general].create_group(specific)
    return hdf_file[general]
