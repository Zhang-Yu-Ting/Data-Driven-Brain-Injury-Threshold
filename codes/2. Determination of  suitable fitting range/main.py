# Before using polynomials to solve for the inflection points of the injury degree-injury 
# threshold curve, it is necessary to determine an appropriate fitting range.
# The impact cases of two types form two composite injury degree-injury threshold curves.
# 50 Head-concrete impacts form the first injury degree curve; 50 Head-football impacts 
# form the second injury degree curve.
# Manually set different fitting ranges, fit the two original curves within these ranges,
# obtain the threshold corresponding the inflection points and fitting goodness, 
# and write them into 'result_all'.
# Based on 'result_all', select the appropriate fitting range with the smallest threshold 
# value error and the largest fitting range under fitting goodness >0.98.

import numpy as np
import os
from fitting_solving_polynomial import fitting_solving
import matplotlib.pyplot as plt

# The number of impact cases for each type of impact.
K = 50

# Extract data.
with open('injury_degree_concrete_MPS', 'r') as data:
    data_c = data.readlines()

with open('injury_degree_football_MPS', 'r') as data:
    data_f = data.readlines()

# thresholds
thres_len   = round(len(data_c)/K - 1)
thresholds  = np.zeros(thres_len, dtype=float)

for ii in range(thres_len):
    
    thresholds[ii] = float(data_c[ii + 1].split()[0])


# Combined injury degree.
injury_degree_c = np.zeros([K, thres_len], dtype=float)
injury_degree_f = np.zeros([K, thres_len], dtype=float)
injury_degree_c_total = np.zeros(thres_len, dtype=float)
injury_degree_f_total = np.zeros(thres_len, dtype=float)

# Add up each cases.
for ii in range(thres_len):

    num_tmp1 = 0
    num_tmp2 = 0

    for jj in range(K):

        injury_degree_c[jj][ii] = float(data_c[jj * (thres_len + 1) + ii + 1].split()[1])
        injury_degree_f[jj][ii] = float(data_f[jj * (thres_len + 1) + ii + 1].split()[1])

        if injury_degree_c[jj][ii] > 0:

            num_tmp1 += 1

        if injury_degree_f[jj][ii] > 0:

            num_tmp2 += 1

    if num_tmp1 > 0:

        for jj in range(K):
            
            injury_degree_c_total[ii] += injury_degree_c[jj][ii]*1/num_tmp1
        

    if num_tmp2 > 0:
         
         for jj in range(K):
            
            injury_degree_f_total[ii] += injury_degree_f[jj][ii]*1/num_tmp2

# plot-two combined relation
fig, ax = plt.subplots(figsize = [3.5,3])
plt.plot(thresholds[11: 122], injury_degree_c_total[11:122],label = 'Hard contact')
plt.plot(thresholds[11: 122], injury_degree_f_total[11:122],label = 'Soft contact')
plt.legend()

plt.xlabel('$T_\mathrm{inj}$', fontsize = 16)
plt.ylabel('$D$', fontsize = 16)
plt.xticks([0.05, 0.2, 0.4, 0.6])
plt.yticks([0, 1, 2])
plt.ylim([-0.05,2])
plt.tick_params(labelsize=16)

plt.tight_layout()
plt.savefig('element_injury_curve_twotype.jpg', dpi = 300)
plt.close()


# Preset multiple fitting ranges
thres_range_min = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
thres_range_max = [0.4, 0.45, 0.5, 0.55, 0.6]

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
        Y_c = injury_degree_c_total[range_l : range_r]
        Y_f = injury_degree_f_total[range_l : range_r]

        Y = [Y_c, Y_f] 

        # Fitting injury degree curves in [tmp_min,tmp_max]
        fitting_solving([X, Y], tmp_min, tmp_max)
        

