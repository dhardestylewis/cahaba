## Methods

The steps and the scripts that produce them

1. Build cahaba Docker image and run Docker container [[Dockerfile](Dockerfile.dev)]
    - A Dockerfile specifies the environment (software tools and versions)
    - The Docker container is used in the following steps
2. Acquire and preprocess data [[acquire_and_preprocess_inputs.py](lib/acquire_and_preprocess_inputs.py)]
    - Download input data
    - Preprocess data
        - Buffer HUC of interest
        - Clip datasets to buffered HUC
        - Rasterize vector layers
3. Produce model datasets required for inundation mapping [[run_by_unit.sh](lib/run_by_unit.sh)]
    - Hydrocondition DEM
        - Burn levees
        - Recondition surface
        - Adjust thalweg
        - Update stream network
    - Make Relative Elevation Model (REM)
        - Generate pixel catchments
        - Level pixel catchments in each reach segment
        - Use Height Above Nearest Drainage (HAND) to create REM grid
    - Make Synthetic Rating Curve (SRC) to relate discharge to stage height
        - Generate reach catchments
        - Compute reach channel geometry
        - Generate SRC based on Manning’s equation
4. Generate flood inundation maps [[inundation.py](tests/inundation.py)]
    - Given a discharge, use SRC to compute stage height
    - Use stage height on REM grid to generate inundation maps

