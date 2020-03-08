# This script merges the 2015-2016 and 1999-2000 NHANES files, so that the trends of actigraphy singular
# spectrum could be analyzed, using regression models

# As the first step, you can download some of the NHANES data files at the following websites:
# https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BPX_I.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/BMX_I.XPT

# https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/DEMO.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/BPX.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/BMX.XPT
#
# For code books and documentation of NHANES, visit https://wwwn.cdc.gov/nchs/nhanes/Default.aspx

import pandas as pd
import numpy as np
import os

# List of file names to merge
xpt_files = ["DEMO_I.XPT", "BPX_I.XPT", "BMX_I.XPT"]

def get_data(year):
    """
    Return the merged data for a given year.
    Currently, the blood pressure data is available for 1999 and 2015.
    The data must be stored into the directory "data/YYYY", where YYYY is the
    four-digit year.
    """

    base = "data/%4d" % year

    if year == 1999:
        xpt_files_use = [x.replace("_I", "") for x in xpt_files]
    else:
        xpt_files_use = xpt_files

    # Retain these variables.
    vars = [
        ["SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH1"],
        ["SEQN", "BPXSY1", "BPXDI1"],
        ["SEQN", "BMXWT", "BMXHT", "BMXBMI", "BMXLEG", "BMXARMC"],
    ]

    # Load each individual file and keep only the variables of interest
    da = []
    for idf, fn in enumerate(xpt_files_use):
        df = pd.read_sas(os.path.join(base, fn))
        df = df.loc[:, vars[idf]]
        da.append(df)

    # SEQN is a common subject ID that can be used to merge the files.
    # These are cross sectional (wide form) files, so there is at most
    # one row per subject.  Subjects may be missing from a file if they
    # did not participate in those assessments.  All subjects should be
    # present in the demog file.

    dx = pd.merge(da[0], da[1], left_on="SEQN", right_on="SEQN")
    dx = pd.merge(dx, da[2], left_on="SEQN", right_on="SEQN")

    # Recode sex as an indicator for female sex
    dx["Female"] = (dx.RIAGENDR == 2).astype(np.int)

    # Recode the ethnic groups
    dx["RIDRETH1"] = dx.RIDRETH1.replace({1: "MA", 2: "OH", 3: "NHW", 4: "NHB", 5: "OR"})

    # Drop rows with any missing data in the variables of interest
    dx = dx.dropna()

    return dx
