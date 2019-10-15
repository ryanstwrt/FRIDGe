import h5py
import os
import fridge.utilities.mcnp_output_scraper as scraper


def create_hdf5_database(database_name, dir=os.getcwd()):
    dt = h5py.string_dtype(encoding='utf-8')
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
        print("New Reactor:" + k)
        reactor = f[k]
        for k1 in reactor.keys():
            raw_reactor = reactor[k1]
            condition = raw_reactor['condition']
            if condition[0] == '900K':
                for k, v in raw_reactor.items():
                    if v[:].dtype == 'object':
                        ds = reactor.create_dataset(k, (len(v),), dtype=dt)
                    else:
                        ds = reactor.create_dataset(k, (len(v),))
                    for l in range(len(v)):
                        ds[l] = v[l]
            elif condition[0] == '600K':
                doppler_keff = raw_reactor['keff'][0]
                doppler_keff_unc = raw_reactor['keff'][1]
                doppler_temp = raw_reactor['temperature']
            else:
                void_keff = raw_reactor['keff'][0]
                void_keff_unc = raw_reactor['keff'][1]

        reactor_keff = reactor['keff'][0]
        temp_dif = doppler_temp - reactor['temperature'][0]
        reactor['doppler_coeff'] = (doppler_keff - reactor_keff) / (reactor_keff * doppler_keff * temp_dif) * pow(10, 5)
        ds = reactor.create_dataset('void_coeff', (1,))
        ds[0] = (void_keff - reactor_keff) / (reactor_keff * void_keff * 99.9) * pow(10, 5)


create_hdf5_database('sfr_db_test',
                     dir=r'C:\Users\ryanstwrt\Documents\OSU\Sodium_Fast_Reactor\PHYSOR2020\Results_Raw')