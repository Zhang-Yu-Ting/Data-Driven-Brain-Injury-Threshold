# Determine the appropriate fitting interval based on the goodness of fit,
# the error of the solution and the fitting range.
# Requirements: 1. The goodness of fit is greater than 0.99;
# 2. On the premise that the fitting range is as large as possible,
# the solution error should be as small as possible.

import numpy as np
import matplotlib.pyplot as plt

with open('results_all', 'r') as data:
    data_0 = data.readlines()

# Total number of fitting range.
num = int(len(data_0)/8)

num_x = np.linspace(1, num, num)

# Preset
thres_err = np.zeros(num, dtype=float)
range_len = np.zeros(num, dtype=float)
R2_sel = np.zeros(num, dtype=float)
pp = []

for ii in range(num):

    jj = ii*8

    range_min = float(data_0[jj].split()[1])
    range_max = float(data_0[jj].split()[3])
    pp.append(str(range_min) +  '-' + str(range_max))

    thres_c = float(data_0[jj + 2].split()[4])
    thres_f = float(data_0[jj + 5].split()[4])

    R2_c = float(data_0[jj + 3].split()[4])
    R2_f = float(data_0[jj + 6].split()[4])

    R2_sel[ii] = min(R2_c, R2_f)

    if R2_sel[ii] >= 0.99:

        thres_err[ii] = abs(thres_c - thres_f)/min(thres_c, thres_f)

        range_len[ii] = range_max -range_min

    else:
        thres_err[ii] = 2
        range_len[ii] = 1

        continue

# Plot
fig, ax = plt.subplots(figsize = [20, 5])
ax1 = ax
ax1.scatter(num_x, thres_err, marker = '*',s = 30, c = '#006400', alpha=0.8)

for i in range(len(num_x)):
    plt.annotate(pp[i], (num_x[i], thres_err[i]))

ax1.set_ylim([0,1])
ax1.set_xlabel('fitting range case', fontsize = 16)
ax1.set_ylabel('Thre_err', c = '#006400', fontsize = 16)
ax1.tick_params(labelsize=16)

ax2 = ax1.twinx()
ax2.scatter(num_x, range_len, c = 'b', alpha=0.5)
ax2.set_ylim([0,0.7])
ax2.set_ylabel('range len', c = 'b', fontsize = 16)
ax2.tick_params(labelsize=16)

plt.tight_layout()
plt.savefig('results.jpg')


