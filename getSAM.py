import os
import requests
import bs4 as bs
import csv
import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#create webdriver
#driver = webdriver.Chrome(r"C:\Users\CommandCenter\AppData\Local\Programs\Python\Python36-32\chromedriver.exe")
driver = webdriver.Chrome(r"C:\Program Files\Python\Python36\chromedriver.exe")

with open("samCheckResult.csv") as csvfileA:
    reader = csv.DictReader(csvfileA)
    with open('samGetResult.csv', 'a') as csvfileB:
        fieldnames = ['SAMResult', 'NAICSCode', 'NAICSdesc']
        writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        for row in reader:
            entryName = (row['SAMResult'])
            if entryName == "Not listed on SAM":
                continue
            driver.get('https://www.sam.gov')
            time.sleep(2)
            driver.get('https://www.sam.gov/SAM/pages/public/searchRecords/search.jsf')
            #get item by id='searchBasicForm:qterm_input'
            content = driver.find_element_by_id('searchBasicForm:qterm_input')
            #type value 8aNameEntry
            #followed by ENTER
            content.send_keys(entryName + '\n')
            time.sleep(1)
            try:
                #get the text that is the h5 child of the the span class= results_body_text
                viewData = driver.find_element_by_xpath('//*[@id="searchResultsID:j_idt159:0:viewDetails"]')
                viewData.click()
                time.sleep(3)
                assertionsButton = driver.find_element_by_id('entitySearchForm:entitySearchassertionReview')
                assertionsButton.click()
                time.sleep(3)
                response = driver.page_source
                soup = bs.BeautifulSoup(response, 'lxml')
                table = soup.findAll('table')[2]
                table = table.findAll('table')[4]
                tbody = table.find('tbody')
                for tr in table.findAll('tr')[1:]:
                    if tr.findAll('td')[1].text == "Yes":
                        NAICScode = tr.findAll('td')[0].text
                        NAICSdesc = tr.findAll('td')[2].text
                print(NAICScode)
                writer.writerow({
                    'SAMResult': entryName,
                    'NAICSCode': NAICScode,
                    'NAICSdesc': NAICSdesc,
                    })
            except NoSuchElementException:
                writer.writerow({
                    'SAMResult': entryName,
                    'NAICSCode': "Not listed",
                    'NAICSdesc': "Not listed",
                                })
##            clearButton = driver.find_element_by_xpath('//*[@id="samContentForm"]/table[2]/tbody/tr[2]/td/input')
##            clearButton.click()
##            time.sleep(1)
            driver.close()
            time.sleep(1)
            driver = webdriver.Chrome(r"C:\Program Files\Python\Python36\chromedriver.exe")

#go to spreadsheet and get company names
#seperate each name into a list

#go to the SAM website
#https://www.sam.gov/SAM/pages/public/searchRecords/search.jsf
#Enter the company name
#Hit enter/search
#check to see if company is listed

#STEP 2
#click view details
