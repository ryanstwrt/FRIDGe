try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='FRIDGe',
    version='1.0.0',
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
        'Programming Language :: Python :: 3.6',
    ],
    license='BSD-3-Clause',
    python_requires='>=3',
    zip_safe=False,
    install_requirements=['PyYAML', 'numpy', 'pytest'],

    packages=['fridge', 'fridge.driver', 'fridge.Assembly', 'fridge.Constituent', 'fridge.test_suite',
              'fridge.utilities', 'fridge.Core', 'fridge.Material'],
    package_dir={
        'fridge': 'fridge',
        'fridge.driver': 'fridge/driver',
        'fridge.test_suite': 'fridge/test_suite',
        'fridge.utilities':  'fridge/utilities',
        'fridge.Assembly': 'fridge/Assembly',
        'fridge.Constituent': 'fridge/Constituent',
        'fridge.Core': 'fridge/Core',
        'fridge.Material': 'fridge/Material'
        },

    include_package_data=True,
)
