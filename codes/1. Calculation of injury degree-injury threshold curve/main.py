# Calculate the whole brain injury degree for a single impact case
# and write it into 'injury_degree_defi_xx'
# Steps:
# 1. Extract response peaks from the raw data.
# 2. Manually set injury thresholds.
# 3. Calculate element injury degrees at different thresholds according
# to the definition of injury degree. The whole brain injury degree is
# then calculated according to its definition.

# Using the brainstem gray matter(part88000105:Gray_Matter_Stem_R)
# elements as an example. In actual calculations, all brain tissue
# elements should be considered.



import numpy as np
import math
from injury_degree_calculation import injury_degree


# 1. Extract response peaks from the raw data.
# Read the raw data into data_0.
with open('88000105', 'r') as datatmp:
    data_0 = datatmp.readlines()

time_len = 501

# Number of elements.
ele_n = int(len(data_0)/time_len - 7)

# The peak response matrix of the element, initial set as a zero matrix.
data_max = np.zeros(ele_n, dtype=float)

# For each element.
for ii in range(ele_n):

    for jj in range(time_len):

        data_max[ii] = float(data_0[6 + ii + jj * (ele_n + 7)].split()[1])


# 2. Manually set injury thresholds.
# Threshold interval.
e = 0.005

# Preset calculation range.
thre_min    =e/100
thre_max    = 1

# Thresholds.
n = math.ceil(thre_max/e)
thresholds = np.linspace(thre_min, thre_max, n + 1)

# 3. Calculate element injury degrees at different thresholds according
# to the definition of injury degree. The whole brain injury degree is
# then calculated according to its definition.
injury_degree(data_max, thresholds)







