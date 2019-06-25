# Running FRIDGe

Running FRIDGe is best done in an interactive python terminal (such as Ipython).
Please note that Python 3.6 or later is required.
Once an Ipython terminal is open in the directory above `fridge` (you should see `docs/`, `fridge/`, `paper/`), and import `fridge_driver` as follows:
```
    import fridge.driver.fridge_driver as fd
```
To run a FRIDGe input file, run the `main` program with the input file name as a string input, as seen below.
**Note:** You do not include the file type.
```
     fd.main('<input file name>')
```
For example the Experimental Breeder II assembly in the [Example](Examples.md) page can be run as follows:
```
     fd.main('EBRII_Driver')
```
The corresponding MCNP input files will be listed in `fridge/mcnp_input_files/` with the given output file name specified in the FRIDGe input file.
