# -*- coding: utf-8 -*-
"""
Spyder Editor

checking how to do this work with Selenium

Robs Fine BS
"""

from selenium import webdriver
driver = webdriver.Chrome('C:\install\chromedriver.exe')
url = 'https://www.seleniumeasy.com/test/basic-first-form-demo.html'
driver.get(url)      
messageField = driver.find_element_by_xpath('//*[@id="user-message"]')
messageField.send_keys('Hello World')
buttonField = driver.find_element_by_xpath('//*[@id="get-input"]/button')
buttonField.click()

messageFielda = driver.find_element_by_xpath('//*[@id="sum1"]')
messageFieldb = driver.find_element_by_xpath('//*[@id="sum2"]')
buttonmathField = driver.find_element_by_xpath('//*[@id="gettotal"]/button')
#Now Send
messageFielda.send_keys('10')
messageFieldb.send_keys('11')
buttonmathField.click()
