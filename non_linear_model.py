import pandas as pd
import numpy as np
import statsmodels.api as sm
from data_prep import get_data
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# pdf = PdfPages("bp_model_2wave.pdf")

dat_1999 = get_data(1999)
dat_2015 = get_data(2015)

# Code year relative to 2000
dat_1999["Year"] = -1
dat_2015["Year"] = 15

dx = pd.concat((dat_1999, dat_2015), axis=0)

def plot_BMI_by_age(result, fml):

    # Create a dataframe with baseline values for all variables
    da = dx.iloc[0:100, :].copy()
    da["RIDAGEYR"] = np.linspace(20, 80, 100)
    da["RIDRETH1"] = "OH"

    plt.figure(figsize=(8, 6))
    plt.clf()
    plt.axes([0.1, 0.3, 0.55, 0.8])
    plt.grid(True)

    for year in -1, 15:
        for female in 0, 1:
            for bmi in 22, 28:

                db = da.copy()
                db.Female = female
                db.BMXBMI = bmi
                db.Year = year

                pr = result.predict(exog=db)

                la = "Female" if female == 1 else "Male"
                la += ", BMI=%.0f" % bmi
                la += ", year=%4d" % (2000 + year)
                plt.plot(da.RIDAGEYR, pr, '-', label=la)

    ha, lb = plt.gca().get_legend_handles_labels()
    leg = plt.figlegend(ha, lb, "center right")
    leg.draw_frame(False)

    plt.xlabel("Age (years)", size=15)
    plt.ylabel("BP (mm/Hg)", size=15)
    plt.title(fml, size=14)
    plt.title(fml, fontdict={"fontsize": 11})
    pdf.savefig()

# Model nonlinear relationship for age and BMI using splines, then allow these curves to be translated
spline1 = "BPXSY1 ~ bs(RIDAGEYR, 4) + bs(BMXBMI, 4) + Female * RIDRETH1 + C(Year)"
model1 = sm.OLS.from_formula(fml1, data=dx)
result1 = model1.fit()
plot_BMI_by_age(result1, fml1)

# Model non-linear relationship for age and BMI using splines, then allow these curves to be translated
spline2 = "BPXSY1 ~ (bs(RIDAGEYR, 4) + bs(BMXBMI, 4) + Female * RIDRETH1) * C(Year)"
model2 = sm.OLS.from_formula(fml2, data=dx)
result2 = model2.fit()
plot_BMI_by_age(result2, fml2)

pdf.close()
