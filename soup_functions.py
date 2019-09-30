from bs4 import BeautifulSoup
import requests
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



def obtain_soup(URL , js = False):

    if js == True:
        return html_r_render(URL)
    return get_soup(URL)

