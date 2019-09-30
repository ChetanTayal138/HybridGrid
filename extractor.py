from generator_data import get_generator_data

UP_URL = "http://www.upsldc.org/real-time-data"



def extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP):
    result_set = []

    for key in dict_UPRVUNL:
        result_set.append((dict_UPRVUNL[key][0],dict_UPRVUNL[key][1],dict_UPRVUNL[key][2],dict_UPRVUNL[key][3],key))


    for key in dict_UPJVNL:
        result_set.append((dict_UPJVNL[key][0],dict_UPJVNL[key][1],dict_UPJVNL[key][2],dict_UPJVNL[key][3],key))


    for key in dict_IPP:
        result_set.append((dict_IPP[key][0],dict_IPP[key][1],dict_IPP[key][2],dict_IPP[key][3],key))


    return result_set


if __name__ == "__main__":

    dict_UPRVUNL, dict_UPJVNL, dict_IPP = get_generator_data(UP_URL)
    result0 = extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP)
    print(result0)
    