# Scripts for analysing XRD measurements
The repository contains notebooks and scripts to perform the azimuthal integration of a scattering pattern.
The scripts were developed in particular for the [XRD instrument](https://www.su.se/department-of-materials-and-environmental-chemistry/research/infrastructure/x-ray-facility-1.606266?open-collapse-boxes=ccbd-singlecrystalxraydiffractometerbrukerd8venture) at Stockholm University.

It is organized as follows:
- `01-notebooks`: You can either use notebooks 01-03 for calibration, intensity integration and for data visualization, or you can use a shorter notebook (05-pyFAI) which contains calibration, intensity integration and visualization all in one.

- `02-scripts`: contains some useful functions for the calcualtion as well as calibrant reference values.
- `03-data`: raw data in `.sfrm` format, not uploaded here.
- `04-processed`: contains the files that are saved as a result of the analysis as well as masks for th detector.
