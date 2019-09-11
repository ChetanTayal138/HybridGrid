from bs4 import BeautifulSoup
import requests
from selenium import webdriver  
from requests_html import HTMLSession


UP_URL = "http://www.upsldc.org/real-time-data"


#Basic operation for obtaining a soup object
def get_soup(URL):
    res = requests.get(URL)
    soup = BeautifulSoup(res.text , "html.parser")
    return soup


#Selenium Render for handling JavaScript
def html_render(URL):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options = options)
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html , "html.parser")
    return soup 


#Only render currently working for obtaining the data from UP SLDC
def html_r_render(URL): 
    session = HTMLSession()
    res = session.get(URL)
    res.html.render()
    soup = BeautifulSoup(res.html.html , 'html.parser')
    return soup 

def get_data(URL , js = False):
    if js == False:
        soupob = get_soup(URL)
    soupob = html_render(URL)

    tables = soupob.findAll("tbody")
    



    table_1 = tables[0]
    sched = table_1.find("td" , {"class":"up_schedule"})
    drawl = table_1.find("td" , {"class":"up_Drawl"})
    od_ud = table_1.find("td" , {"class":"up_OD_UD"})
    dmnd  = table_1.find("td" , {"class":"up_Demand"})
    dict_1 = {
                "Schedule(MW)":int(sched.text), 
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




    NPCL = tables[-1]
    NPCL_sched  = NPCL.find("td" , {"class" : "npcl_sg"})
    NPCL_actual = NPCL.find("td" , {"class" : "npcl_act"})
    NPCL_OD_UD  = NPCL.find("td" , {"class" : "npcl_diff"})


    dict_NPCL = { 
                    "Schedule(MW)" : int(NPCL_sched.text),
                    "Actual(MW)" : int(NPCL_actual.text),
                    "NPCL_OD_UD(MW)" : int(NPCL_OD_UD.text)
                }


    dict_UPRVUNL = {}

    UPRVUNL = soupob.find("tbody" , {"class" , "td-header_1"} )
    UPRVUNL_rows = UPRVUNL.findAll("tr")  
    shown_rows = UPRVUNL.findAll("tr" , {"class" : "clTot"})
    for i in shown_rows:
        values = i.findAll("td")
        gen_name   = values[0].text
        gen_dc     = values[1].text
        gen_sched  = values[2].text
        gen_actual = values[3].text
        gen_oi_ui  = values[4].text
        dict_UPRVUNL[f'{gen_name}'] = [gen_dc , gen_sched , gen_actual , gen_oi_ui]

    
    print(dict_UPRVUNL) 
    

    print("SUCCESS!")
    return [dict_1,dict_2,dict_3]

 
if __name__ == "__main__":
    get_data(UP_URL , js = True)
    