# Plot fitting results based on 'inflection_points_all_for_plot_defi_1_0.05_0.6'.

import matplotlib.pyplot as plt

def plot1(file_name, case_num, nn, path):

    # Read data.
    with open(file_name, 'r') as data:
        data = data.readlines()

    # X coordinate.
    X = [4, 5, 6, 7, 8]

    # Preset Y_all and R_all.
    Y_all = []
    R_all = []

    for ii in range(len(case_num)):

        # For a sort of combiantions.
        Y_combinations_all = []
        R_combinations_all = []

        for jj in range(nn):


            Y_tmp = []
            R_tmp = []

            tt = 1 + ii * 61 + 1 + 3 * jj

            tmp1 = data[tt + 1].split()[1:]
            tmp2 = data[tt + 2].split()[1:]

            for tmpdata in tmp1:
                Y_tmp.append(float(tmpdata))

            for tmpdata in tmp2:
                R_tmp.append(float(tmpdata))


            Y_combinations_all.append(Y_tmp)
            R_combinations_all.append(R_tmp)

            del Y_tmp
            del R_tmp

        Y_all.append(Y_combinations_all)
        R_all.append(R_combinations_all)

        del Y_combinations_all
        del R_combinations_all


    # Plot.
    # For each specific combination
    for ii, combinations_all in enumerate(Y_all):

        # Y refers to the 3-7th results obtained for a specific curve.
        for jj, Y in enumerate(combinations_all):

            path1 = path + '\\' + str(case_num[ii]) + '_' + 'cases'+ '\\' + 'combination_'+ str(jj)

            fig, ax = plt.subplots(figsize = [6, 4])

            ax1 = ax
            ax1.plot(X, Y, marker = '*', c = '#006400')
            ax1.set_yticks([-0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5])
            ax1.set_xlabel('Fitting degree', fontsize = 16)
            ax1.set_ylabel('$T_\mathrm{inj}$', fontsize = 16)
            ax1.tick_params(labelsize=15)

            ax2 = ax1.twinx()
            ax2.scatter(X, R_all[ii][jj], c = 'orange')
            ax2.set_yticks([0.95, 0.96, 0.97, 0.98, 0.99, 1])
            ax2.set_ylabel('Goodness of fit', fontsize = 16)
            ax2.tick_params(labelsize=15)

            plt.xticks([4, 5, 6, 7, 8])
            plt.title(str(case_num[ii]) + ' cases combination_' + str(jj + 1), fontsize = 16)
            plt.tight_layout()
            plt.savefig(path1 + '\\' + 'fitting_results.jpg')
            plt.close()

    # A summary of each category of combinations.
    for ii, combinations_all in enumerate(Y_all):

        fig, ax = plt.subplots(figsize = [6, 4])
        ax1 = ax
        ax2 = ax1.twinx()

        path1 = path + '\\' + str(case_num[ii]) + '_' + 'cases'

        for jj, Y in enumerate(combinations_all):

            ax1.plot(X, Y, marker = '*', c = '#006400')
            ax1.set_xticks([])
            ax1.set_yticks([])

            ax2.scatter(X, R_all[ii][jj], c = 'orange')
            ax2.set_xticks([])
            ax2.set_yticks([])

        ax1.set_yticks([-0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5])
        ax1.set_xlabel('Fitting degree', fontsize = 16)
        ax1.set_ylabel('$T_\mathrm{inj}$', fontsize = 16)
        ax1.tick_params(labelsize=15)
        ax2.set_yticks([0.9, 0.96, 0.98, 0.99, 1])
        ax2.set_ylabel('Goodness of fit', fontsize = 16)
        ax2.tick_params(labelsize=15)
        plt.xticks([4, 5, 6, 7, 8])
        plt.title(str(case_num[ii]) + ' cases combination', fontsize = 16)
        plt.tight_layout()
        plt.savefig(path1 + '\\' + 'fitting_results_all.jpg')
        plt.close()



