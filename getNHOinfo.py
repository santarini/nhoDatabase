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

with open("test.csv") as csvfileA:
    reader = csv.DictReader(csvfileA)
    with open('Result.csv', 'a') as csvfileB:
        fieldnames = ['8a', 'SAMResult']
        writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        for row in reader:
            entryName = (row['8a'])
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
                CollegeName = driver.find_element_by_xpath('//*[@id="searchResultsID:dataTable"]/table[1]/tbody/tr/td/table/tbody/tr/td/li/table/tbody/tr/td/table[1]/tbody/tr/td[2]/span/h5')
                writer.writerow({
                    '8a': entryName,
                    'SAMResult': CollegeName.text
                    })
            except NoSuchElementException:
                writer.writerow({
                                '8a': entryName,
                                'SAMResult': "ERROR"
                                })
            driver.close()
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
