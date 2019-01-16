"""
+----------------------------------------------------------------+
 | Program: weedMapsDispensaries.py                                          |
 | Module Purpose: Gets all the doctors info by state and stores |
 |                 it into a CSV                                 |
 | Author: Hugo Iriarte                                          |
 +---------------------------------------------------------------+
"""
#Imports
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#URL change sate
url = ('https://weedmaps.com/dispensaries/in/united-states/california')

#Variables holding Disprndstird Data
name = [] #h1
number = [] #styled-components__MetadataLink-ieqye3-11
address = [] #styled-components__ListingHeroMapAddressRow-sc-1hnyeii-3
email = [] #styled-components__MetadataLink-ieqye3-11
website = [] #styled-components__MetadataLink-ieqye3-11
stateLicense = [] #styled-components__LicensesListWrapper-sc-1qmu0u8-1

#initiate driver
chromedriver = 'C:/Users/Henry/Desktop/chromedriver'
driver = webdriver.Chrome(chromedriver)
#Get the URL
driver.get(url)
driver.implicitly_wait(20)
#Element Holding Doctors Profile URL
elements = driver.find_elements_by_class_name('no-decoration') 
#Array of doctor profile URL
arrayURL = [] 

#For loop to append all the URL the arrayURL variable
for i in elements:
    x = i.get_attribute("href") 
    arrayURL.append(x)

#Loop through all doctor profile url's
for i in arrayURL:
    chromedriver = 'C:/Users/Henry/Desktop/chromedriver'
    driver = webdriver.Chrome(chromedriver)
    driver.get(i)
    driver.implicitly_wait(20)
    #Exception to handle if popup comes up to verify if over 18
    try:
        popup = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div[1]/button')
        popup.click()
    except NoSuchElementException as exception:
        print("Element not found and test failed")
    #Open div to get dispensary data
    openUp = driver.find_element_by_class_name('styled-components__Toggle-jk6o0a-12')
    openUp.click()
    #Dispensary Name
    dispensaryName = driver.find_element_by_tag_name('h1').text
    name.append(dispensaryName)
    #Dispensary Number, Email, Website
    data = driver.find_elements_by_class_name('styled-components__MetadataLink-ieqye3-11')
    if len(data) == 4:
        number.append(data[0].text)
        email.append(data[2].text)
        website.append(data[3].text)
    elif len(data) == 3:
        number.append(data[0].text)
        email.append(data[2].text)
        website.append(' ')
    #Dispensary address
    a = []
    location = driver.find_elements_by_class_name('styled-components__ListingHeroMapAddressRow-sc-1hnyeii-3')
    for i in location:
        a.append(i.text)
    b = a[0] + a[1]
    address.append(b)
    #Dispensary License number
    try:
        licenses = driver.find_element_by_class_name("styled-components__LicensesListWrapper-sc-1qmu0u8-1").text
        n = licenses.replace('\n', ' ')
        stateLicense.append(n)
    except NoSuchElementException as exception:
        print("Element not found and test failed")
        stateLicense.append(' ')
    #Close driver
    driver.quit()

#Length of data pulled
loopCSV = len(name)

#Makes a file with all the data and puts it into columns
with open('C:/Users/Henry/Documents/pythonCSV/californiaDispensaries.csv', 'w', newline='') as f:
    fieldNames = ['Dispensary Name', 'Number', 'Address', 'Email', 'Website', 'State License', 'Initiated By', 'Company']
    thewriter = csv.DictWriter(f, fieldnames = fieldNames)
    thewriter.writeheader()
    for i in range(loopCSV):
        thewriter.writerow({'Dispensary Name' : name[i], 'Number' : number[i], 'Address' : address[i], 'Email' : email[i], 'Website' : website[i], 'State License' : stateLicense[i], 'Initiated By' : 'Ray', 'Company' : name[i]})