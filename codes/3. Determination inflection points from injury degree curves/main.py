# Solve for the threshold values corresponding to the inflection points of 
# the combined injury degree curves within the previously determined fitting range.

import numpy as np
import os
from fitting_solving_polynomial import fitting_solving
from combination import combination
from plot1 import plot1

# Total number of impact cases.
K = 50 * 2

# The number of cases which form the combined injury degree curve.
case_num = [2, 10, 20, 40, 60]

# The number of samples in each combination.
nn = 20

# Extract the current folder path.
path = os.path.dirname(os.path.abspath(__file__))

# Combine cases, and write to files.
combination(case_num, nn, K, path)

# thresholds
with open('injury_degree_defi_1_both_MPS', 'r') as data:
    data = data.readlines()

thres_len   = round(len(data)/K - 1)
thresholds  = np.zeros(thres_len, dtype=float)

for ii in range(thres_len):
    
    thresholds[ii] = float(data[ii + 1].split()[0])

# Start and end values of the fitting range.
thres_range_min = 0.04
thres_range_max = 0.6


for ii, tmp in enumerate(thresholds):

    if tmp < thres_range_min:
        
        continue

    else:

        range_l = ii
        break

for ii, tmp in enumerate(thresholds):

    if tmp < thres_range_max:
        
        continue

    else:

        range_r = ii
        break


# Fitting results files
file_name1 = path + '\\' + 'fitting_results_all_defi_1' + '_' + str(thres_range_min) + '_' + str(thres_range_max)
file_name2 = path + '\\' + 'inflection_points_all_for_plot_defi_1' + '_' + str(thres_range_min) + '_' + str(thres_range_max)


with open(file_name1, 'a') as datatmp:
    datatmp.writelines('Within a given fitting range, fitting the original curve and calculating the inflection points, the whole results are below.\n')
    
with open(file_name2, 'a') as datatmp:
    datatmp.writelines('Within a given fitting range, fitting the original curve and calculating the inflection points, the points are below.\n')
    

# For different sets of combinations.
for jj in range(len(case_num)):

    with open(file_name1, 'a') as datatmp:
        datatmp.writelines(str(case_num[jj]) + '_cases\n')

    with open(file_name2, 'a') as datatmp:
        datatmp.writelines(str(case_num[jj]) + '_cases\n')
    
    # For each curve.
    for kk in range(nn):

        with open(file_name1, 'a') as datatmp:
            datatmp.writelines('combination ' + str(kk) + '\n')

        with open(file_name2, 'a') as datatmp:
            datatmp.writelines('combination ' + str(kk) + '\n')

        # Read the data.
        path1 = path + '\\' + str(case_num[jj]) + '_' + 'cases'+ '\\' + 'combination_'+ str(kk)

        with open(path1 + '\\' + 'combination_'+ str(kk), 'r') as data:
            data = data.readlines()

        Y_all = np.zeros(len(data) - 1, dtype=float)

        for ll in range(len(data) - 1):

            Y_all[ll] = data[ll + 1].replace('\n', '')

        # Cut the data
        X = thresholds[range_l : range_r]
        Y = Y_all[range_l : range_r]

        # Solve and plot.
        fitting_solving([X, Y], [thres_range_min, thres_range_max], file_name1, file_name2, path1)

# Plot.
plot1(file_name2, case_num, nn, path)



