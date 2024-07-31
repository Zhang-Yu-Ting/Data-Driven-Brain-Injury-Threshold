# Plot all the results corresponding to the 5th fit 
# (distinguish whether the points with R2 less than 0.98, and plot the points with error bars in one graph)

import numpy as np
import os
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.ticker import MultipleLocator
from matplotlib.font_manager import FontProperties


plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['text.usetex'] = True

# Extract the current folder path.
path = os.path.dirname(os.path.abspath(__file__))

path1 = path + '\\inflection_points_all_for_plot_0.04_0.5'

with open(path1, 'r') as data:
    data = data.readlines()

# concrete + football
case_num = [5, 10, 20, 40, 60]

nn = 20

case_num_plot = [0, 1, 2, 3, 4]

# plot1 represents the left vertical coordinate
# plot2 represents the right vertical coordinate
# 1 and 2 in x1 and x2 represent the selected fit and excluded fit respectively.

plot1_x1 = []
plot1_x2 = []
plot2_x1 = []
plot2_x2 = []
plot1_y1 = []
plot1_y2 = []
plot2_y1 = []
plot2_y2 = []

for jj in range(20):

    Y_tmp_1 = []
    R_tmp_1 = []
    Y_tmp_2 = []
    R_tmp_2 = []
    
    for ii in range(len(case_num)):

        tt = 1 + ii * 61 + 1 + 3 * jj

        R_tmp = float(data[tt + 2].split()[1])

        if R_tmp >= 0.98:

            tmp1_1 = float(data[tt + 1].split()[1])
            tmp2_1 = float(data[tt + 2].split()[1])
            plot1_x1.append(case_num_plot[ii])
            plot1_y1.append(tmp1_1)
            plot2_x1.append(case_num_plot[ii])
            plot2_y1.append(tmp2_1)
            

        else:

            tmp1_2 = float(data[tt + 1].split()[1])
            tmp2_2 = float(data[tt + 2].split()[1])
            plot1_x2.append(case_num_plot[ii])
            plot1_y2.append(tmp1_2)
            plot2_x2.append(case_num_plot[ii])
            plot2_y2.append(tmp2_2)
            
    del Y_tmp_1
    del R_tmp_1
    del Y_tmp_2
    del R_tmp_2

#Mean and standard error of the selcted points
Y_ave = np.zeros(len(case_num), dtype=float)
std_error = np.zeros(len(case_num), dtype=float)

for ii in range(len(case_num)):

    # A set of Y combinations
    Y_tmp = []
    n = 0

    for jj in range(nn):

        tt = 1 + ii * 61 + 1 + 3 * jj
        
        R_tmp = float(data[tt + 2].split()[1])
        # print(R_tmp)

        if R_tmp >= 0.98:

            Y_tmp.append(float(data[tt + 1].split()[1]))
            n += 1
            # print(R_tmp)

    # print(Y_tmp)
    
    Y = np.array(Y_tmp)

    # Calculate standard error
    if n > 0:

        Y_ave[ii] =  np.mean(Y) 
        Y_std = np.std(Y)
        std_error[ii] = Y_std / np.sqrt(n)

# Record data
for ii, tmp in enumerate(Y_ave):
    with open('Mean + standard error', 'a') as datatmp:
        datatmp.writelines(str(case_num[ii]) + '  ' + str(tmp) + '  ' + str(std_error[ii]) + '\n')

X1 = [5, 10, 20, 40, 60]
X_tmp = range(len(X1))

# plot
plt.rc('font', family = 'Times New Roman')
fig, ax = plt.subplots(figsize = [6, 3])
ax1 = ax
ax2 = ax1.twinx()


ax2.scatter(plot2_x1, plot2_y1, marker = '^', c = 'steelblue', label='$R^{2}\geq 0.98$', s=40, alpha=0.3, zorder = 1)
ax1.scatter(plot1_x1, plot1_y1, marker = '^', c = 'black', label='Selected', s = 40, alpha=0.3, zorder=2)
ax1.errorbar(case_num_plot, Y_ave, yerr = std_error, fmt = '^', ms = 4, mec = 'orange', ecolor = 'orange', label='Mean of selected',  color = 'black', elinewidth=1, capsize=4, capthick = 0.5, zorder = 3)
ax2.scatter(plot2_x2, plot2_y2, marker = 'x', c = 'steelblue', label='$R^{2}<0.98$', s=45, alpha=0.3, zorder = 1)
ax1.scatter(plot1_x2, plot1_y2, marker = 'x', c = 'black', label='Excluded', s = 45, alpha=0.3, zorder=2)

# Get the legend handles and labels for both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Merge legend handles and labels
handles = handles1 + handles2
labels = labels1 + labels2

# Custom legend order
custom_order = [3, 0, 2, 4, 1] 

font_prop = FontProperties(family='Times New Roman', size='large')

# Adjust legend position and font size
fig.legend([handles[idx] for idx in custom_order], 
           [labels[idx] for idx in custom_order], 
           loc='center left', bbox_to_anchor=(0.65, 0.6), prop=font_prop)


ax1.set_yticks([0, 0.1, 0.2, 0.3, 0.4])
ax1.set_xlabel('$K$', fontsize = 16)
ax1.set_ylabel('$T_\mathrm{inj,crit}$', fontsize = 16)
ax1.tick_params(labelsize=16)

ax2.set_yticks([0.9, 0.98, 1])
ax2.set_ylabel('$R^{2}$', fontsize = 16)
ax2.tick_params(labelsize=16)
ax2.spines['right'].set_color('steelblue')

plt.xticks(X_tmp, X1)
plt.tight_layout()
plt.subplots_adjust(right=0.5)
plt.savefig(path + '\\' + 'All_5th_with_errorbar.jpg', dpi=1200)
plt.close()
