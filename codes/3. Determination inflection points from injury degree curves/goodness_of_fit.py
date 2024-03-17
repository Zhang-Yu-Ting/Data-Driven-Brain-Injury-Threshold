def goodness_of_fit(data, fitting_data):


    y_mean = sum(data) / len(data)

    s_list =[(y - y_mean)**2 for y in data]
    sst = sum(s_list)

    s_list =[(y - y_mean)**2 for y in fitting_data]
    ssr = sum(s_list)

    rr = ssr /sst
    return rr
