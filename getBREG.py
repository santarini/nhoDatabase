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

with open("BREGcheckResult.csv") as csvfileA:
    reader = csv.DictReader(csvfileA)
    with open('BREGGetResult.csv', 'a') as csvfileB:
        fieldnames = ['8a', 'BREGResult', 'Officers']
        writer = csv.DictWriter(csvfileB, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        for row in reader:
            officerString = ""
            entryName = (row['8a'])
            fileNo = (row['BREGResult'])
            if fileNo == "Not in search" or fileNo == "Withdrawn" or fileNo == "Expired" or fileNo == "Several filings":
                continue
            driver.get('https://hbe.ehawaii.gov/documents/business.html?fileNumber=' + fileNo + '&view=officers')
            response = driver.page_source
            soup = bs.BeautifulSoup(response, 'lxml')
            #try:
            tableDiv = soup.find("div", {"class": "tabContent"})
            table = tableDiv.find('table')
            tableBody = table.find('tbody')
            for tr in table.findAll('tr')[1:]:
                officerName = tr.findAll('td')[0]
                officerTitle = tr.findAll('td')[1]
                officerString = officerString + officerName.text + " " + officerTitle.text + "; "
            writer.writerow({
                '8a': entryName,
                'BREGResult': fileNo,
                'Officers': officerString
                })
##            except IndexError:
##                writer.writerow({
##                    '8a': entryName,
##                    'BREGResult': "Not in search"
##                    })
##                print(entryName + ': Not in search query')
##            except NoSuchElementException and IndexError:
##                writer.writerow({
##                    '8a': entryName,
##                    'BREGResult': "Not entity"
##                    })
##                print(entryName + ': Not active')
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
