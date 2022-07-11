import parameters
from function import getEmail, getUrl
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
sleep(2)

driver.get('https://www.google.com')
sleep(1)

search_query = driver.find_element('name', 'q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(1)

pageUrl_list = []
# get profile urls as a list
url_list = []

#get first search result's profile urls
getUrl(driver, url_list)


#get urls of other search pages
page_source = BeautifulSoup(driver.page_source, "lxml")
page_source = page_source.find("div", class_="GyAeWb")
page_source = page_source.find("div", role="navigation")
links = page_source.findAll("a")
for link in links :
    link_href = link.get('href')
    pageUrl_list.append(link_href)
# print(pageUrl_list)


#get profile urls from pages one by one starting from page 2
#till page 10
for i in range(len(pageUrl_list)-1): 
    driver.get('https://www.google.com' + pageUrl_list[i])
    getUrl(driver, url_list)

print(url_list)
print(len(url_list))



name_list = []
location_list = []
email_list = []
for url in url_list[:20]:
    driver.get(url)
    sleep(1)   #set delay to load the data
    page_source = BeautifulSoup(driver.page_source, "lxml")
    info_div = page_source.find("div", class_="ph5")
    name = info_div.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words").get_text().strip()
    location = info_div.find("span", class_="text-body-small inline t-black--light break-words").get_text().strip()
    name_list.append(name)
    location_list.append(location)
    email = getEmail(driver)
    email_list.append(email)
    print(name + ', '+ location + ', ' + email) 

# print(name_list)
# print(location_list)
# print(email_list)



