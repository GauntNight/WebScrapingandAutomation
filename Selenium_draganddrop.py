# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 14:44:22 2019

Selenium Drag and Drop Test

@author: peterro2
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome('C:\install\chromedriver.exe')
driver.maximize_window()
url = 'http://dhtmlgoodies.com/scripts/drag-drop-custom/demo-drag-drop-3.html'
driver.get(url)
boxStockholm = driver.find_element_by_xpath('//*[@id="box2"]')
boxWashington = driver.find_element_by_xpath('//*[@id="box3"]')
homeWashington = driver.find_element_by_xpath('//*[@id="box103"]')
homeStockholm = driver.find_element_by_xpath('//*[@id="box102"]')
actions = ActionChains(driver)
actions.drag_and_drop(boxWashington, homeWashington)
actions.drag_and_drop(boxStockholm, homeStockholm).perform()