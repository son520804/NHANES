# NHANES
This repository stores the Python codes (partial) for the course project National Health and Nutrition Examination Survey Actigraphy Singular Spectrum and Regression Analysis

Dataset:
For each year between 1999 and 2015, the NHANES data are stored in multiple separate files, all of which are in XPT (SAS transport/export) format. Nicely, both Python and R are compatibe to read this SAS data format. 
Within each wave, there is one file for each group of attributes. Those separate files collaboratively capture various aspects of the health issues of the U.S. population and purport for cross-sectional study. Within a wave, the “sequence number” variable SEQN uniquely identifies one person (primary key). Different files from the same wave can be linked together by joining the unique SEQN values. 

Study:
This project examines how individual's risk factors and demographics affect actigraphy. We propose statistical models which take actigraphy as the dependent variable, and risk factors (Diastolic Blood Pressure, Systolic Blood Pressure, High-density Lipoprotein, Low-density Lipoprotein, Triglycerides) and demographics (Non-smoke, age, height, weight, ethnicity) as independent variables.

Documentation:
The detailed NHANES data and documentation are available at https://wwwn.cdc.gov/nchs/nhanes/Default.aspx
