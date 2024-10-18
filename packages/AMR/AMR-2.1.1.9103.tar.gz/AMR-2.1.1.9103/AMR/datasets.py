BLUE = '\033[94m'
GREEN = '\033[32m'
RESET = '\033[0m'

print(f"{BLUE}AMR:{RESET} Setting up R environment and AMR datasets...", flush=True)

from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr, isinstalled
import pandas as pd
# import importlib.metadata as metadata

# Check if AMR package is installed in R
if not isinstalled('AMR'):
    utils = importr('utils')
    utils.install_packages('AMR', repos='https://msberends.r-universe.dev')

# Python package version of AMR
python_amr_version = metadata.version('AMR')
# R package version of AMR
# r_amr_version = robjects.r('packageVersion("AMR")')[0]

# Compare R and Python package versions
# if r_amr_version != python_amr_version:
#     print(f"{BLUE}AMR:{RESET} Version mismatch detected. Updating AMR R package version to {python_amr_version}...", flush=True)
#     try:
#         # Re-install the specific version of AMR in R
#         utils = importr('utils')
#         utils.install_packages('AMR', repos='https://msberends.r-universe.dev')
#     except Exception as e:
#         print(f"{BLUE}AMR:{RESET} Could not update: {e}{RESET}", flush=True)

# Activate the automatic conversion between R and pandas DataFrames
pandas2ri.activate()

# example_isolates
example_isolates = pandas2ri.rpy2py(robjects.r('''
df <- AMR::example_isolates
df[] <- lapply(df, function(x) {
    if (inherits(x, c("Date", "POSIXt", "factor"))) {
        as.character(x)
    } else {
        x
    }
})
df <- df[, !sapply(df, is.list)]
df
'''))
example_isolates['date'] = pd.to_datetime(example_isolates['date'])

# microorganisms
microorganisms = pandas2ri.rpy2py(robjects.r('AMR::microorganisms[, !sapply(AMR::microorganisms, is.list)]'))
antibiotics = pandas2ri.rpy2py(robjects.r('AMR::antibiotics[, !sapply(AMR::antibiotics, is.list)]'))
clinical_breakpoints = pandas2ri.rpy2py(robjects.r('AMR::clinical_breakpoints[, !sapply(AMR::clinical_breakpoints, is.list)]'))

print(f"{BLUE}AMR:{RESET} {GREEN}Done.{RESET}", flush=True)
