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
    with open('BREGcheckResult.csv', 'a') as csvfileB:
        fieldnames = ['8a', 'BREGResult']
        writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        for row in reader:
            entryName = (row['8a'])
            entryNameCleaned = entryName
            for v in (".", ",", "Inc", "LLC", "`"):
                entryNameCleaned = entryNameCleaned.replace(v, "")
            entryNameCleaned = entryNameCleaned.replace(" ", "+")
            driver.get('https://hbe.ehawaii.gov/documents/search.html?recordType=ALL&entityType=ALL&status=ALL&beginsWith=true&query=' + entryNameCleaned)
            response = driver.page_source
            soup = bs.BeautifulSoup(response, 'lxml')
            try:
                table = soup.findAll('table')[4]
                tableBody = table.find('tbody')
                for tr in table.findAll('tr')[1:]:
                    if tr.findAll('td')[1].text == "Entity" and tr.findAll('td')[3].text == "Active":
                        fileNo = tr.findAll('td')[2].text
                writer.writerow({
                    '8a': entryName,
                    'BREGResult': fileNo.replace(' ','')
                    })
                print(entryName + ': ' + fileNo.replace(' ',''))
            except IndexError:
                writer.writerow({
                    '8a': entryName,
                    'BREGResult': "Not in search"
                    })
                print(entryName + ': Not in search query')
            except NoSuchElementException and IndexError:
                writer.writerow({
                    '8a': entryName,
                    'BREGResult': "Not entity"
                    })
                print(entryName + ': Not active')
            #driver.close()
            #driver = webdriver.Chrome(r"C:\Program Files\Python\Python36\chromedriver.exe")

#go to spreadsheet and get company names
#seperate each name into a list

#go to the SAM website
#https://www.sam.gov/SAM/pages/public/searchRecords/search.jsf
#Enter the company name
#Hit enter/search
#check to see if company is listed

#STEP 2
#click view details
