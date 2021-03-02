import os

# Environmental variables and constants.
BENCHMARK_CATEGORIES = ['ble', 'nws', 'usgs', 'ifc']
TEST_CASES_DIR = r'/data/test_cases/'
PREVIOUS_FIM_DIR = r'/data/previous_fim'
OUTPUTS_DIR = os.environ['outputDataDir']
INPUTS_DIR = r'/data/inputs'
AHPS_BENCHMARK_CATEGORIES = ['usgs', 'nws']
FR_BENCHMARK_CATEGORIES = ['ble', 'ifc']
PRINTWORTHY_STATS = ['CSI', 'TPR', 'TNR', 'FAR', 'MCC', 'TP_area_km2', 'FP_area_km2', 'TN_area_km2', 'FN_area_km2', 'contingency_tot_area_km2', 'TP_perc', 'FP_perc', 'TN_perc', 'FN_perc']
GO_UP_STATS = ['CSI', 'TPR', 'MCC', 'TN_area_km2', 'TP_area_km2', 'TN_perc', 'TP_perc', 'TNR']
GO_DOWN_STATS = ['FAR', 'FN_area_km2', 'FP_area_km2', 'FP_perc', 'FN_perc']

MAGNITUDE_DICTIONARY = {'ble': ['100yr', '500yr'],
                        'ifc': ['10yr', '25yr', '50yr', '100yr', '200yr', '500yr'],
                        'nws': ['action', 'minor', 'moderate', 'major'],
                        'usgs': ['action', 'minor', 'moderate', 'major']
        }


# Colors.
ENDC = '\033[m'
TGREEN_BOLD = '\033[32;1m'
TGREEN = '\033[32m'
TRED_BOLD = '\033[31;1m'
TWHITE = '\033[37m'
WHITE_BOLD = '\033[37;1m'
CYAN_BOLD = '\033[36;1m'
