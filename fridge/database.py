import h5py
import os
import glob
import numpy
import fridge.mcnp_output_scraper as scraper


def create_hdf5_database(database_name, dir=os.getcwd()):
    f = h5py.File(database_name + '.h5', 'w')
    # create the initial database with raw values
    for root, dirs, files in os.walk(dir):
        for file in files:
            if '.out' in file:
                try:
                    scraper.translate_output(root, f, file)
                except ValueError:
                    print("Entry for {} already entered, skipping {} from directory {}.".format(file, file, root))

    #set the attributes for the reactor type
    for k in f.keys():
        reactor = f[k]
        for k1 in reactor.keys():
            raw_reactor = reactor[k1]
            condition = raw_reactor.attrs['condition']
            if condition == b'900K':
               for attr, val in raw_reactor.attrs.items():
                    reactor.attrs.create(attr, val)
            elif condition == b'600K':
                doppler_keff = raw_reactor.attrs['keff'][0]
                doppler_keff_unc = raw_reactor.attrs['keff'][1]
                doppler_temp = raw_reactor.attrs['temperature']
            else:
                void_keff = raw_reactor.attrs['keff'][0]
                void_keff_unc = raw_reactor.attrs['keff'][1]

        reactor_keff = reactor.attrs['keff'][0]
        temp_dif = doppler_temp - reactor.attrs['temperature']
        reactor.attrs['doppler_coeff'] = (doppler_keff - reactor_keff) / (reactor_keff * doppler_keff * temp_dif) * pow(10, 5)
        reactor.attrs['void_coeff'] = (void_keff - reactor_keff) / (reactor_keff * void_keff * 99.9) * pow(10, 5)


    for k in f.keys():
        reactor = f[k]
        print()
        print(k)
        for k1, v1 in reactor.attrs.items():
            print(k1, v1)


create_hdf5_database('height_smear_db',
                     dir=r'C:\Users\ryanstwrt\Documents\OSU\Sodium_Fast_Reactor\PHYSOR2020\height_smear_results')