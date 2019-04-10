try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='FRIDGe',
    version='0.1.1',
    description='Fast Reactor Input Deck Generator (FRIDGe) is a general purpose fast reactor MCNP input deck creator. '
                'It will read in material/geometry files and create a fast reactor subassembly. Future iterations will '
                'be able to incoporate physical phenomena, smears, and full core creation.',
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

    packages=['fridge', 'frdige.driver', 'fridge.Assembly', 'fridge.Constituent', 'fridge.test_suite',
              'fridge.utilities'],
    package_dir={
        'fridge': 'fridge',
        'fridge.driver': 'fridge/driver',
        'fridge.test_suite': 'fridge/test_suite',
        'fridge.utilities':  'fridge/utilities',
        'fridge.Assembly': 'fridge/Assembly',
        'fridge.Constituent': 'frdige/Constituent'
        },

    include_package_data=True,
    package_data={
        'fridge.data.CotN': ['data/CotN/*.yaml'],
        'fridge.data.assembly': ['data/assembly/*.yaml'],
        'fridge.data.materials': ['data/materials/*.yaml'],
        'fridge.fridge_input_file': ['fridge_input_file/*.yaml']
    },
)
