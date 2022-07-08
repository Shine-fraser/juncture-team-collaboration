import parameters
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
sleep(3)

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
    sleep(2)
    page_source = BeautifulSoup(driver.page_source, "lxml")
    info_div = page_source.find("div", class_="ph5 pb5")
    name = page_source.find("h1", "text-heading-xlarge").get_text()
    location = info_div.find("span", class_="text-body-small inline t-black--light break-words").get_text().strip()

    #get contact info link first
    contact = page_source.find_all("a", id_="top-card-text-details-contact-info")
    contact.get('href')
    name_list.append(name)
    location_list.append(location)


# contact_list = []
# driver.get(url_list[0])
# sleep(2)
# page_source = BeautifulSoup(driver.page_source, "lxml")
# contact = page_source.find(class_="ember-view link-without-visited-state cursor-pointer text-heading-small inline-block break-words", href=True)
# contact = contact.get('href')
# driver.get(contact)
