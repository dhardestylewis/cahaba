## Cahaba: Flood Inundation Mapping for U.S. National Water Model

Flood inundation mapping (FIM) software configured to work with the U.S. National Water Model operated and maintained by the National Oceanic and Atmospheric Administration (NOAA) National Weather Service (NWS). Software enables inundation mapping capability by generating Relative Elevation Models (REMs) and Synthetic Rating Curves (SRCs). Included are tests to evaluate skill and computational efficiency as well as functions to generate inundation maps.

This project is organized as follows:
1. Build and run cahaba/FIM Docker image/container
    - A Dockerfile specifies the environment (software tools and versions)
    - The Docker container is used in the following steps
2. Acquire and preprocess data
    - Download input data
    - Preprocess data
        - Buffer HUC of interest
        - Clip datasets to buffered HUC
        - Rasterize vector layers
    - Hydrocondition DEM
        - Burn levees
        - [AGREE](https://www.caee.utexas.edu/prof/maidment/gishydro/ferdi/research/agree/agree.html)
        - Adjust thalweg
    - Update stream network
3. Make Relative Elevation Model (REM) grid
    - Generate pixel catchments
    - Level pixel catchments in each reach segment
    - Use Height Above Nearest Drainage (HAND) to create REM grid
4. Make Synthetic Rating Curve (SRC) to relate discharge to stage height
    - Generate reach catchments
    - Compute reach channel geometry
    - Generate SRC based on Manning’s equation
5. Generate inundation maps
    - Given a discharge, use SRC to compute stage height
    - Use stage height on REM grid to generate inundation maps

Additionally, tools were developed to evaluate the inundation maps
- The inundation map is compared to a benchmark dataset
- Contingency metrics are produced and common model performance statistics are computed

----

## Results/Outputs

Examples of outputs to be added here


----

## Installation and Usage

Instructions for installing, configuring, and running the project can be found [here](INSTALL.md)

----

## Getting Involved

NOAA's National Water Center welcomes anyone to contribute to the Cahaba repository to improve flood inundation mapping capabilities. For more details see [CONTRIBUTING.md](CONTRIBUTING.md). Please contact Fernando Aristizabal (fernando.aristizabal@noaa.gov) or Fernando Salas (fernando.salas@noaa.gov) to get started.

## Open Source Licensing Info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)

----

## Credits and References
1. Office of Water Prediction [(OWP)](https://water.noaa.gov/)
2. National Flood Interoperability Experiment [(NFIE)](https://web.corral.tacc.utexas.edu/nfiedata/)
3. Garousi‐Nejad, I., Tarboton, D. G.,Aboutalebi, M., & Torres‐Rua, A.(2019). Terrain analysis enhancements to the Height Above Nearest Drainage flood inundation mapping method. Water Resources Research, 55 , 7983–8009. https://doi.org/10.1029/2019WR0248375.
4. Zheng, X., D.G. Tarboton, D.R. Maidment, Y.Y. Liu, and P. Passalacqua. 2018. “River Channel Geometry and Rating Curve Estimation Using Height above the Nearest Drainage.” Journal of the American Water Resources Association 54 (4): 785–806. https://doi.org/10.1111/1752-1688.12661.
5. Liu, Y. Y., D. R. Maidment, D. G. Tarboton, X. Zheng and S. Wang, (2018), "A CyberGIS Integration and Computation Framework for High-Resolution Continental-Scale Flood Inundation Mapping," JAWRA Journal of the American Water Resources Association, 54(4): 770-784, https://doi.org/10.1111/1752-1688.12660.
6. Barnes, Richard. 2016. RichDEM: Terrain Analysis Software. http://github.com/r-barnes/richdem
7. [TauDEM](https://github.com/dtarb/TauDEM)
8. Federal Emergency Management Agency (FEMA) Base Level Engineering [(BLE)](https://webapps.usgs.gov/infrm/estBFE/)
9. Verdin, James; Verdin, Kristine; Mathis, Melissa; Magadzire, Tamuka; Kabuchanga, Eric; Woodbury, Mark; and Gadain, Hussein, 2016, A software tool for rapid flood inundation mapping: U.S. Geological Survey Open-File Report 2016–1038, 26 p., http://dx.doi.org/10.3133/ofr20161038.
10. United States Geological Survey (USGS) National Hydrography Dataset Plus High Resolution (NHDPlusHR). https://www.usgs.gov/core-science-systems/ngp/national-hydrography/nhdplus-high-resolution
