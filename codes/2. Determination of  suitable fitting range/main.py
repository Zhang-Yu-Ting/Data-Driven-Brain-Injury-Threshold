# Before using polynomials to solve for the inflection points of the injury degree-injury
# threshold curve, it is necessary to determine an appropriate fitting range.
# The impact cases of two types form two composite injury degree-injury threshold curves.
# 50 Head-concrete impacts form the first injury degree curve; 50 Head-football impacts
# form the second injury degree curve.
# Manually set different fitting ranges, fit the two original curves within these ranges,
# obtain the threshold corresponding the inflection points and fitting goodness,
# and write them into 'result_all'.
# Based on 'result_all', select the appropriate fitting range with the smallest threshold
# value error and the highest fitting goodness.

import numpy as np
import os
from fitting_solving_polynomial import fitting_solving

# The number of impact cases for each type of impact.
K = 50

# Extract data.
with open('injury_degree_defi_1_concrete_MPS', 'r') as data:
    data_c = data.readlines()

with open('injury_degree_defi_1_football_MPS', 'r') as data:
    data_f = data.readlines()

# thresholds
thres_len   = round(len(data_c)/K - 1)
thresholds  = np.zeros(thres_len, dtype=float)

for ii in range(thres_len):

    thresholds[ii] = float(data_c[ii + 1].split()[0])


# Combined injury degree.
injury_degree_c = np.zeros(thres_len, dtype=float)
injury_degree_f = np.zeros(thres_len, dtype=float)

# Add up each cases.
for ii in range(thres_len):

    for jj in range(K):

        injury_degree_c[ii] += float(data_c[jj * (thres_len + 1) + ii + 1].split()[1])*1/K
        injury_degree_f[ii] += float(data_f[jj * (thres_len + 1) + ii + 1].split()[1])*1/K


# Preset multiple fitting ranges
thres_range_min = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
thres_range_max = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75]

# Fit curves to find the inflection points and record.
for ii, tmp_max in enumerate(thres_range_max):

    for jj, tmp_min in enumerate(thres_range_min):

        for kk, tmp in enumerate(thresholds):

            if tmp < tmp_min:

                continue

            else:

                range_l = kk
                break

        for kk, tmp in enumerate(thresholds):

            if tmp < tmp_max:

                continue

            else:

                range_r = kk
                break

        X = thresholds[range_l : range_r]
        Y_c = injury_degree_c[range_l : range_r]
        Y_f = injury_degree_f[range_l : range_r]

        Y = [Y_c, Y_f]

        # Fitting injury degree curves in [tmp_min,tmp_max]
        fitting_solving([X, Y], tmp_min, tmp_max)


