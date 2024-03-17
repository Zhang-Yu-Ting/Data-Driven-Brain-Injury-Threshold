# Calculate the injury degree.

import numpy as np
import copy as c


def injury_degree(data, thresholds):

    # For each threshold.
    for ii, threshold_tmp in enumerate(thresholds):

        # Select peak responses greater than the threshold.
        data_injury         = data[data > threshold_tmp]

        if len(data_injury) > 0:

            # Calculate the injury degree, considering three alpha values, which are 1, 2, and 3.
            injury_degree_1  = (data_injury - threshold_tmp)/threshold_tmp

            injury_degree_2 = ((data_injury - threshold_tmp)/threshold_tmp)**2

            injury_degree_3 = ((data_injury - threshold_tmp)/threshold_tmp)**3

            # The whole brain injury degree.
            injury_degree_1_ave = np.mean(injury_degree_1)

            with open('injury_degree_defi_1', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   ' + str(injury_degree_1_ave) + '\n')

            injury_degree_2_ave = np.mean(injury_degree_2)

            with open('injury_degree_defi_2', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   ' + str(injury_degree_2_ave) + '\n')

            injury_degree_3_ave = np.mean(injury_degree_3)

            with open('injury_degree_defi_3', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   ' + str(injury_degree_3_ave) + '\n')

        else:

            with open('injury_degree_defi_1', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   0\n')

            with open('injury_degree_defi_2', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   0\n')

            with open('injury_degree_defi_3', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   0\n')
        