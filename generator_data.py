from soup_functions import html_r_render , get_soup

UP_URL = "http://www.upsldc.org/real-time-data"



######## FUNCTION FOR OBTAINING THE GENERATOR DATA FROM DIFFERENT CATEGORIES ###################

def get_generator_data(URL):


    soupob = html_r_render(URL)
    #soupob = obtain_soup(URL,js = True)
    dict_UPRVUNL = {}
    
    ############### DATA FOR UPRVUNL ##################


    UPRVUNL = soupob.find("tbody" , {"class" : "td-header_1"} )
    UPRVUNL_rows = UPRVUNL.findAll("tr")  
    shown_rows = UPRVUNL.findAll("tr" , {"class" : "clTot"})
    for i in shown_rows:
        values = i.findAll("td")
        gen_name   = values[0].text
        gen_dc     = values[1].text
        gen_sched  = values[2].text
        gen_actual = values[3].text
        gen_oi_ui  = values[4].text
        dict_UPRVUNL[f'{gen_name}'] = list(map(float,[gen_dc , gen_sched , gen_actual , gen_oi_ui]))    

    ####################################################




    ############## DATA FOR UPJVNL ###########

    dict_UPJVNL = {}

    UPJVNL = soupob.find("tbody" , {"class" : "td-header_2"})
    UPJVNL_rows = UPJVNL.findAll("tr")
    shown_rows = UPJVNL.findAll("tr" , {"class" : "clTot"})
    for i in shown_rows:
        values = i.findAll("td")
        gen_name   = values[0].text
        gen_dc     = values[1].text
        gen_sched  = values[2].text
        gen_actual = values[3].text
        gen_oi_ui  = values[4].text
        dict_UPJVNL[f'{gen_name}'] = list(map(float, [gen_dc , gen_sched , gen_actual , gen_oi_ui]))

    #################################################


    ################ DATA FOR IPP #######################

    dict_IPP = {}

    IPP = soupob.find("tbody" , {"class" : "td-header_3"})
    IPP_rows = IPP.findAll("tr")
    shown_rows = IPP.findAll("tr" , {"class" : "clTot"})
    for i in shown_rows:
        values = i.findAll("td")
        gen_name   = values[0].text
        gen_dc     = values[1].text
        gen_sched  = values[2].text
        gen_actual = values[3].text
        gen_oi_ui  = values[4].text
        dict_IPP[f'{gen_name}'] = list(map(float, [gen_dc , gen_sched , gen_actual , gen_oi_ui]))

  
    
    return [dict_UPRVUNL, dict_UPJVNL, dict_IPP]






if __name__ == "__main__":
    print(get_generator_data(UP_URL))
    