from bs4 import BeautifulSoup
from time import sleep
import re

def getUrl(driver, url_list):
    linkedin_urls = driver.find_elements('xpath', "//div[@class='yuRUbf']/a")
    for url in linkedin_urls:
        profile_url = url.get_attribute("href")
        if('linkedin.com/in' in profile_url):  # check if url is real profile url or not
            url_list.append(url.get_attribute("href"))

    return url_list



def getEmail(driver):
    #"https://www.linkedin.com/in/chandramouleeswaran-sankaran-mouli-b174611?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BPA9pZzzBSMyQrD2hcyjEQw%3D%3D"
    
    page_source = BeautifulSoup(driver.page_source, "lxml")
    contact_info = page_source.find(
        class_="ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words", href=True)
    contact_info = contact_info.get('href')
    # print(contact_info)

    #get email from Contact Info
    driver.get("https://linkedin.com" + contact_info)
    sleep(1)   #set delay to load the data
    page_source = BeautifulSoup(driver.page_source, "lxml")
    try:
        info_div = page_source.find("div", id="artdeco-modal-outlet")
        email = info_div.find(class_="pv-contact-info__contact-link link-without-visited-state t-14", href=re.compile("mailto:"))
        email = email.get('href')[7:]
    except:
        email = 'none'
    return email

