# Calculate the injury degree.

import numpy as np
import copy as c


def injury_degree(data, thresholds):  

    # For each threshold.
    for ii, threshold_tmp in enumerate(thresholds):

        # Select peak responses greater than the threshold.
        data_injury         = data[data > threshold_tmp]

        if len(data_injury) > 0:

            # Calculate the injury degree in a impact case.
            injury_degree  = (data_injury - threshold_tmp)/threshold_tmp

            # The whole brain injury degree.
            injury_degree_ave = np.mean(injury_degree)
            
            with open('injury_degree', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   ' + str(injury_degree_ave) + '\n')

        else:
            
            with open('injury_degree', 'a') as datatmp:
                datatmp.writelines(str(threshold_tmp) + '   0\n')

            