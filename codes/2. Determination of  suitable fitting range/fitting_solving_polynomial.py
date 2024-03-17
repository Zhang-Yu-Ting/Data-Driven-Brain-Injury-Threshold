import numpy as np
import sympy as sp
from goodness_of_fit import goodness_of_fit

def fitting_solving(data, tmp_min, tmp_max):

    # Two types
    sorts = ['concrete', 'football']
    
    # The degree of polynomial fitting.
    fitting_num = [3, 4, 5, 6, 7]

    R_thres = 0.99

    with open('results_all', 'a') as datatmp:
        datatmp.writelines('\n' + 'fitting_range ' + str(tmp_min) + ' - ' + str(tmp_max) + '\n')
         

    for ww in range(2):

        point_selected = []
        point_all = []
        R = []

        for ii in range(len(fitting_num)):

            p1 = np.polyfit(data[0], data[1][ww], fitting_num[ii])

            
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
            diff2_fit_func  = np.poly1d(d2_coefficient)
            fit_Y           = func_Y(data[0])

            # Calculate the goodness of fit.
            R_tmp = goodness_of_fit(data[1][ww], fit_Y)
            

            # Calculate the inflection point of the fitting curve.
            x_solution = sp.solve(f2, x)

            # If there is no solution.
            if x_solution == []:

                point_selected.append('none')
                point_all.append(-0.1)
                R.append(R_tmp)
                continue

            else:

                R.append(R_tmp)
 
                # Convert the data type to complex numbers.
                solution = [complex(item) for item in x_solution]

                w = 0

                point_selected_tmp = []
                for jj, tmp0 in enumerate(solution):

                    if abs(np.imag(tmp0)) < 1e-10:

                        w = 1

                        tmp = np.real(tmp0)

                        if tmp > tmp_min and tmp < tmp_max:

                            if tmp <= tmp_min*1.05 or tmp >= tmp_max *0.95:

                                continue

                            elif diff2_fit_func(tmp - tmp/100) < 0:

                                continue

                            else:

                                point_selected_tmp.append(tmp)

                                continue
                        
                        else:

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

        # Record the results for 3rd, 4th, 5th, 6th, and 7th degrees.
        with open('results_all', 'a') as datatmp:
            datatmp.writelines(sorts[ww] + '\n')
            datatmp.writelines('inflection_points   ' + str('%.4g' %point_all[0]) + ' ' + str('%.4g' %point_all[1]) + ' ' + str('%.4g' %point_all[2]) + ' ' + str('%.4g' %point_all[3]) + ' ' + str('%.4g' %point_all[4])  + '\n' )
            datatmp.writelines('              R^2   ' + str('%.4g' %R[0]) + ' ' + str('%.4g' %R[1]) + ' ' + str('%.4g' %R[2]) + ' ' + str('%.4g' %R[3]) + ' ' + str('%.4g' %R[4]) + '\n')


        
        

                    

            

                
                
                