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
import re

#create webdriver
#driver = webdriver.Chrome(r"C:\Users\CommandCenter\AppData\Local\Programs\Python\Python36-32\chromedriver.exe")
#driver = webdriver.Chrome(r"C:\Program Files\Python\Python36\chromedriver.exe")

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
            print(entryNameCleaned)
