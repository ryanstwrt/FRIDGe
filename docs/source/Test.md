# Testing FRIDGe

FRIDGe has an a test suite built that can be run to ensure all of the packages are operating correctly.
To run the test suite, open a terminal in the fridge directory and perform the following:

```
python -m pytest
```

This should run all of the files in `fridge/test_suite`.
There are currently 82 tests which will run; this typically takes between 5 ad d30 seconds.
This will generate four MCNP input files in `fridge/mcnp_input_files`.
**Note:** There are four MCNP input files with the preface `Prefab_`, these are four MCNP input files that the test suite is checking against.
**DO NOT** alter these files in any way, otherwise some of the tests will likely fail.
