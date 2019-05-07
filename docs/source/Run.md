# Running FRIDGe

Running FRIDGe is best done in an interactive python terminal (such as ipython).
Once an Ipython terminal is open in the `fridge` directory, import `fridfe_driver` as follows:
```
    import fridge.driver.fridge_driver as fd
```
To run a FRIDGe input file, run the `main` program with the input file name as a string input, as seen below.
Note: You do not include the file type.
```
     fd.main('<input file name>')
```
For example the EBRII assembly that was created in the previous section can be run as follows:
```
     fd.main('EBRII_Driver')
```
Users can now continue to make material, assembly, core, and FRIDGe input files.
These corresponding MCNP input files will be listed in `/fridge/mcnp_input_files/` with the given output file name specified in the FRIDGe input file.
