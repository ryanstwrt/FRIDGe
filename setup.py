try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='FRIDGe',
    version='0.1.0',
    description='Fast Reactor Input Deck Generator is a general purpose fast reactor MCNP input deck creator. It will read in material/geometry files and create a fast reactor subassembly. Future iterations will be able to incoporate physical phenomena, smears, and full core creation.',
    author='Ryan Stewart',
    author_email='stewryan@oregonstat.edu',
    url='https://github.com/ryanstwrt/FRIDGe',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Reactor Designer',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    license='BSD-3-Clause',
    python_requires='>=3',
    zip_safe=False,
    packages=['fridge', 'frdige.driver', 'fridge.input_readers', 'fridge.Test_Suite', 'fridge.utilities'],
    # or find automatically:
    package_dir={
        'fridge': 'fridge',
        'fridge.driver': 'fridge/driver',
        'fridge.input_readers': 'fridge/input_readers',
        'fridge.Test_Suite': 'fridge/Test_Suite',
        'fridge.utilities':  'fridge/utilities'
        },

    package_data={
        'fridge': ['CotN/*.txt'],
        'fridge': ['Geometry/*.txt'],
        'fridge': ['Materials/*.txt'],
    },
)