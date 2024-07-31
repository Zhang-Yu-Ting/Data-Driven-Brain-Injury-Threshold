# Randomly select impact cases for combinations and write to files. 

import numpy as np
import random
import os


def combination(case_num, nn, K, path):

    with open('injury_degree_both_MPS', 'r') as data:
        data = data.readlines()

    thres_len           = round(len(data)/K - 1)
    injury_degree       = np.zeros([K, thres_len], dtype=float)

    for ii in range(thres_len):

        for jj in range(K):

            injury_degree[jj][ii]       = float(data[jj * (thres_len + 1) + ii + 1].split()[1])

    # Case number.
    cases = np.linspace(1,100,100)
    cases = [int(tmp) for tmp in cases]

    # Combine cases.
    for ii, tmp_case_num in enumerate(case_num):
        
        for jj in range(nn):

            Y = np.zeros(thres_len, dtype=float)

            # Randomly select case number.
            cases_tmp = random.sample(cases, tmp_case_num)

            path1 = path + '\\' + str(tmp_case_num) + '_' + 'cases'+ '\\' + 'combination_'+ str(jj)
            if not os.path.exists(path1):
                os.makedirs(path1)

            for kk in range(thres_len):

                num_tmp1 = 0

                for ll, cases_tmptmp in enumerate(cases_tmp):

                    if injury_degree[ll][kk] > 0:

                        num_tmp1 += 1

                    else:
                        continue

                if num_tmp1 > 0:
                    
                    for ll, cases_tmptmp in enumerate(cases_tmp):

                        Y[kk] += injury_degree[cases_tmptmp - 1][kk] / num_tmp1

                else:
                    continue

            with open(path1 + '\\' + 'combination_'+ str(jj), 'a') as data:
                data.writelines('The combination of impact cases are ' + str(cases_tmp) + '\n')
            
            for kk, tmpdata in enumerate(Y):

                with open(path1 + '\\' + 'combination_'+ str(jj), 'a') as data:
                    data.writelines(str(tmpdata) + '\n')
