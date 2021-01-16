## Methods

The steps and the scripts that produce them

1. Build and run cahaba/FIM Docker image/container [Dockerfile]
    - A Dockerfile specifies the environment (software tools and versions)
    - The Docker container is used in the following steps
2. Acquire and preprocess data [acquire_and_preprocess_inputs.py]
    - Download input data
    - Preprocess data
        - Buffer HUC of interest
        - Clip datasets to buffered HUC
        - Rasterize vector layers
3. Hydrocondition DEM [run_by_unit.sh]
    - Burn levees
    - Recondition surface (using [AGREE](https://www.caee.utexas.edu/prof/maidment/gishydro/ferdi/research/agree/agree.html))
    - Adjust thalweg
    - Update stream network
3. Make Relative Elevation Model (REM) grid [run_by_unit.sh]
    - Generate pixel catchments
    - Level pixel catchments in each reach segment
    - Use Height Above Nearest Drainage (HAND) to create REM grid
4. Make Synthetic Rating Curve (SRC) to relate discharge to stage height [run_by_unit.sh]
    - Generate reach catchments
    - Compute reach channel geometry
    - Generate SRC based on Manning’s equation
5. Generate inundation maps [inundation.py]
    - Given a discharge, use SRC to compute stage height
    - Use stage height on REM grid to generate inundation maps

