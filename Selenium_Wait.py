# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:01:11 2019

Testing Wait and other web driver conditions

@author: peterro2
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.google.com/earth'
driver = webdriver.Chrome('C:\install\chromedriver.exe')
driver.get(url)
wait = WebDriverWait(driver, 5)
googleButton = '/html/body/div/div/div[2]/div/div[4]/a[3]/span/span'
wait.until(EC.element_to_be_clickable((By.XPATH, googleButton)))
googleclickButton = driver.find_element_by_xpath(googleButton)
googleclickButton.click()