import parameters
import re
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
s = Service('C:\\Users\\computer\\Downloads\\chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)


driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element('id', 'session_key')
# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)


# locate password form by_class_name
password = driver.find_element('id', 'session_password')
# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)


# locate submit button by_class_name
log_in_button = driver.find_element(
    'class name', 'sign-in-form__submit-button')
# .click() to mimic button click
log_in_button.click()
sleep(3)

driver.get('https://www.google.com')
sleep(1)

search_query = driver.find_element('name', 'q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(2)

# get profile urls as a list
linkedin_urls = driver.find_elements('xpath', "//div[@class='yuRUbf']/a")
url_list = []
for url in linkedin_urls:
    profile_url = url.get_attribute("href")
    if('linkedin.com/in' in profile_url):  # check if url is real profile url or not
        url_list.append(url.get_attribute("href"))
print(url_list)


name_list = []
location_list = []

for url in url_list:
    driver.get(url)
    sleep(2)   #set delay to load the data
    page_source = BeautifulSoup(driver.page_source, "lxml")
    info_div = page_source.find("div", class_="ph5 pb5")
    name = info_div.find("h1", class_="text-heading-xlarge").get_text().strip()
    location = info_div.find("span", class_="text-body-small inline t-black--light break-words").get_text().strip()
    name_list.append(name)
    location_list.append(location)
print(name_list)
print(location_list)


#get Contact Info link from a profile 
driver.get("https://www.linkedin.com/in/chandramouleeswaran-sankaran-mouli-b174611?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BPA9pZzzBSMyQrD2hcyjEQw%3D%3D")
sleep(2)   #set delay to load the data
page_source = BeautifulSoup(driver.page_source, "lxml")
contact_info = page_source.find(
    class_="ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words", href=True)
contact_info = contact_info.get('href')
print(contact_info)



#get email from Contact Info
driver.get("https://linkedin.com" + contact_info)
sleep(2)   #set delay to load the data
page_source = BeautifulSoup(driver.page_source, "lxml")
info_div = page_source.find("div", id="artdeco-modal-outlet")
email = info_div.find(class_="pv-contact-info__contact-link link-without-visited-state t-14", href=re.compile("mailto:"))
email = email.get('href')[7:]
print(email)