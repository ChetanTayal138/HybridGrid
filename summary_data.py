from soup_functions import html_r_render

UP_URL = "http://www.upsldc.org/real-time-data"


######## FUNCTION FOR OBTAINING THE SUMMARY DATA  ###################

def get_summary_data(URL):

    soupob = html_r_render(URL)
    #soupob = obtain_soup(URL , js = True)
    tables = soupob.findAll("tbody")

    ############ SUMMARY DATA ############

    table_1 = tables[0]
    sched = table_1.find("td" , {"class":"up_schedule"})
    drawl = table_1.find("td" , {"class":"up_Drawl"})
    od_ud = table_1.find("td" , {"class":"up_OD_UD"})
    dmnd  = table_1.find("td" , {"class":"up_Demand"})
    dict_1 = {
                "Schedule(MW)":float(sched.text), 
                "Drawl(MW)":int(drawl.text), 
                "OD/UD(MW)":int(od_ud.text), 
                "Demand(MW)":int(dmnd.text)
            }


    table_2 = tables[1]
    total_ssgs    = table_2.find("td" , {"class":"Total_SSGS"})
    up_therm_gen  = table_2.find("td" , {"class":"UP_Thermal_Generation"})
    ipp_therm_gen = table_2.find("td" , {"class":"IPP_Thermal_Generation"})
    hydro_gen     = table_2.find("td" , {"class":"UP_Hydro_Generation"})
    
    dict_2 = {
                "Total SSGS(MW)": int(total_ssgs.text),
                "UP Thermal Generation" : int(up_therm_gen.text),
                "IPP Thermal Generation" : int(ipp_therm_gen.text),
                "UP Hydro Generation" : int(hydro_gen.text)
            }

    table_3 = tables[2]
    cpp_gen   = table_3.find("td" , {"class":"Co-gen"})
    solar_gen = table_3.find("td" , {"class":"solar"})
    frequency = table_3.find("td" , {"class":"Frequency"})
    dev_rate  = table_3.find("td" , {"class":"Deviation-rate"})
    
    dict_3 = {
                "Co-gen/CPP Generation(MW)": int(cpp_gen.text),
                "RE/Solar Generation(MW)" : int(solar_gen.text),
                "Frequency(Hz)" : float(frequency.text),
                "Deviation Rate (Paise/Unit)" : float(dev_rate.text)
            }



        ############## DATA FOR NPCL ####################

    NPCL = tables[-1]
    NPCL_sched  = NPCL.find("td" , {"class" : "npcl_sg"})
    NPCL_actual = NPCL.find("td" , {"class" : "npcl_act"})
    NPCL_OD_UD  = NPCL.find("td" , {"class" : "npcl_diff"})


    dict_NPCL = { 
                    "Schedule(MW)" : int(NPCL_sched.text),
                    "Actual(MW)" : int(NPCL_actual.text),
                    "NPCL_OD_UD(MW)" : int(NPCL_OD_UD.text)
                }



   ###################################################


    return [dict_1 , dict_2 , dict_3 , dict_NPCL]




if __name__ == "__main__":
    print(get_summary_data(UP_URL))


