# Use different polynomials to fit the damage degree-damage threshold curves, and record the solution results.

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from goodness_of_fit import goodness_of_fit

def fitting_solving(data, thres_range, file_name1, file_name2, path1):

    # The degree of polynomial fitting.
    fitting_num = [4, 5, 6, 7, 8]

    R_thres = 0.99

    point_selected = []
    point_all = []
    R = []

    for ii in range(len(fitting_num)):

        p1 = np.polyfit(data[0], data[1], fitting_num[ii])


        # Solve for complex roots and extract the real parts from them.
        x = sp.symbols('x')

        fit_func = 0
        for tt in range(fitting_num[ii] + 1):

            fit_func += p1[tt] * x ** (fitting_num[ii] - tt)

        f2 = sp.diff(fit_func, x, 2)

        d1_coefficient = []
        d2_coefficient = []

        for jj in range(fitting_num[ii]):
            d1_coefficient.append(p1[jj] * (fitting_num[ii] - jj))

        for jj in range(fitting_num[ii] - 1):
            d2_coefficient.append(p1[jj] * (fitting_num[ii] - jj) * (fitting_num[ii] - jj - 1))

        func_Y          = np.poly1d(p1)
        diff_fit_func   = np.poly1d(d1_coefficient)
        diff2_fit_func  = np.poly1d(d2_coefficient)
        fit_Y           = func_Y(data[0])
        diff_Y_fit      = diff_fit_func(data[0])
        diff2_Y_fit     = diff2_fit_func(data[0])

        # Calculate the goodness of fit.
        R_tmp = goodness_of_fit(data[1], fit_Y)

        # Plot
        fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = [10, 3])

        ax1 = ax[0]
        ax1.plot(data[0], data[1])
        ax1.plot(data[0], fit_Y)
        ax1.set_xlabel('$T_\mathrm{inj}$', fontsize = 16)
        ax1.set_ylabel('D', fontsize = 16)
        ax1.tick_params(labelsize=15)
        ax1.text(0.4, 0.8, 'R$^{2}$ = ' + '%.3g' %R_tmp, transform = ax1.transAxes, fontsize = 16)

        ax2 = ax[1]
        ax2.plot(data[0], diff_Y_fit)
        ax2.set_xlabel('$T_\mathrm{inj}$', fontsize = 16)
        ax2.set_ylabel('D\'', fontsize = 16)
        ax2.tick_params(labelsize=15)

        ax3 = ax[2]
        ax3.plot(data[0], diff2_Y_fit)
        Y0 = [0]*len(data[0])
        ax3.plot(data[0], Y0, linestyle = '--')
        ax3.set_xlabel('$T_\mathrm{inj}$', fontsize = 16)
        ax3.set_ylabel('D\'\'', fontsize = 16)
        ax3.tick_params(labelsize=15)

        plt.tight_layout()
        plt.xticks()
        plt.savefig(path1 + '\\' + str(fitting_num[ii]) + '.jpg')
        plt.close()


        # Calculate the inflection point of the fitting curve.
        x_solution = sp.solve(f2, x)

        # If there is no solution.
        if x_solution == []:

            with open(file_name1, 'a') as datatmp:
                datatmp.writelines(str(fitting_num[ii]) + '   ' + 'no inflection point   ' + 'R^2 = ' + str(R_tmp) + '\n')

            point_selected.append('none')
            point_all.append(-0.1)
            R.append(R_tmp)
            continue

        else:

            R.append(R_tmp)


            # Record results.
            with open(file_name1, 'a') as datatmp:
                datatmp.writelines(str(fitting_num[ii]) + '   original_results_all\n')


            # Write down the real solutions.
            # Select points corresponding to local maxima of the first detivaive, marked as 1;
            # Points corresponding to local minima of the first derivative, marked as 0-2;
            # Results within 5% of the ends of the fitting range, marked as 0-1.
            # Solutions beyond the ends of the fitting, marked as 0-0.

            # Convert the data type to complex numbers.
            solution = [complex(item) for item in x_solution]

            w = 0

            point_selected_tmp = []
            for jj, tmp0 in enumerate(solution):

                # print(np.imag(tmp0))
                if abs(np.imag(tmp0)) < 1e-10:

                    w = 1

                    tmp = np.real(tmp0)

                    if tmp > thres_range[0] and tmp < thres_range[1]:

                        if tmp <= thres_range[0]*1.05 or tmp >= thres_range[1] *0.95:

                            with open(file_name1, 'a') as datatmp:
                                datatmp.writelines('          ' + str('%.4g' %tmp) + '    0-1\n')

                            continue

                        elif diff2_fit_func(tmp - tmp/100) < 0:

                            with open(file_name1, 'a') as datatmp:
                                datatmp.writelines('          ' + str('%.4g' %tmp) + '    0-2\n')

                            continue

                        else:

                            with open(file_name1, 'a') as datatmp:
                                datatmp.writelines('          ' + str('%.4g' %tmp) + '    1\n')

                            point_selected_tmp.append(tmp)

                            continue

                    else:

                        with open(file_name1, 'a') as datatmp:
                                datatmp.writelines('          ' + str('%.4g' %tmp) + '    0-0\n')

                        continue

                else:
                    continue

            if len(point_selected_tmp) >= 1:

                point_all.append(min(point_selected_tmp))

            else:
                point_all.append(-0.1)



            if R_tmp > R_thres:

                if len(point_selected_tmp) >= 1:

                    point_selected.append(min(point_selected_tmp))

                else:

                    point_selected.append('none')

            else:

                point_selected.append('none')

            if w == 0:

                with open(file_name1, 'a') as datatmp:
                    datatmp.writelines('no inflection point   ' + 'R^2 = ' + str('%.4g' %R_tmp) + '\n')

            else:

                # After all the solutions have been recorded, the next line records the R^2 of this fit.
                with open(file_name1, 'a') as datatmp:
                    datatmp.writelines('    R^2 = ' + str('%.4g' %R_tmp) + '\n')


    # Record the results for 3rd, 4th, 5th, 6th, and 7th degrees.
    with open(file_name2, 'a') as datatmp:
        datatmp.writelines('inflection_points   ' + str('%.4g' %point_all[0]) + ' ' + str('%.4g' %point_all[1]) + ' ' + str('%.4g' %point_all[2]) + ' ' + str('%.4g' %point_all[3]) + ' ' + str('%.4g' %point_all[4])  + '\n' )
        datatmp.writelines('              R^2   ' + str('%.4g' %R[0]) + ' ' + str('%.4g' %R[1]) + ' ' + str('%.4g' %R[2]) + ' ' + str('%.4g' %R[3]) + ' ' + str('%.4g' %R[4]) + '\n')











                