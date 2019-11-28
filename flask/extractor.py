from generator_data import get_generator_data,get_generator_names


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





def create_generators():

    UPRVUNL_dict = {}
    UPJVNL_dict = {}
    IPP_dict = {}
    UPRVUNL_list, UPJVNL_list, IPP_list = get_generator_names()

    
    for gen in UPRVUNL_list:
        UPRVUNL_dict[gen] = {
            "DC" : [],
            "Schedule" : [],
            "Actual" : [],
            "OI_UI" : []
        }

    for gen in UPJVNL_list:
        UPJVNL_dict[gen] = {
            "DC" : [],
            "Schedule" : [],
            "Actual" : [],
            "OI_UI" : []
        }

    for gen in IPP_list:
        IPP_dict[gen] = {
            "DC" : [],
            "Schedule" : [],
            "Actual" : [],
            "OI_UI" : []
        }


    return [UPRVUNL_dict, UPJVNL_dict, IPP_dict]







if __name__ == "__main__":
    
    print(create_generators())
    dict_UPRVUNL, dict_UPJVNL, dict_IPP = get_generator_data(UP_URL)
    result0 = extract_result_set(dict_UPRVUNL, dict_UPJVNL, dict_IPP)
    print(result0)
        




