import h5py
import os
import glob
import numpy
import fridge.mcnp_output_scraper as scraper


def create_hdf5_database(database_name, dir=os.getcwd()):
    f = h5py.File(database_name + '.h5', 'w')
    for root, dirs, files in os.walk(dir):
        for file in files:
            if '.out' in file:
                try:
                    scraper.translate_output(root, f, file)
                except ValueError:
                    print("Entry for {} already entered, skipping {} from directory {}.".format(file, file, root))
    for k in f.keys():
        print(k)

create_hdf5_database('test_db', dir=r'C:\Users\ryanstwrt\Documents\OSU\Sodium_Fast_Reactor\PHYSOR2020\Results_Raw')