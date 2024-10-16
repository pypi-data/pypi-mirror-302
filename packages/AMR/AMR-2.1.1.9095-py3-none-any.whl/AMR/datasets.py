BLUE = '\033[94m'
GREEN = '\033[32m'
RESET = '\033[0m'

print(f"{BLUE}AMR:{RESET} Setting up R environment and AMR datasets...", flush=True)

from rpy2 import robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr, isinstalled
import pandas as pd

# Check if the R package is installed
if not isinstalled('AMR'):
    utils = importr('utils')
    utils.install_packages('AMR')

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
df
'''))
example_isolates['date'] = pd.to_datetime(example_isolates['date'])

# microorganisms
microorganisms = pandas2ri.rpy2py(robjects.r('AMR::microorganisms[, !sapply(AMR::microorganisms, is.list)]'))
antibiotics = pandas2ri.rpy2py(robjects.r('AMR::antibiotics[, !sapply(AMR::antibiotics, is.list)]'))
clinical_breakpoints = pandas2ri.rpy2py(robjects.r('AMR::clinical_breakpoints'))

print(f"{BLUE}AMR:{RESET} {GREEN}Done.{RESET}", flush=True)
