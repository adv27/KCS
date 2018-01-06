import csv
import io
import sys

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

PATH_TO_CHROME_DRIVER = r'C:\Users\vdanh\Desktop\robotframework_tuturial\WebDemo\webdriver\Window\chromedriver'
URL = r'http://192.168.1.1'
URL_INFORMATION = r'https://192.168.1.1/device_status.cgi'
keys = ['ProductClass',
        'Vendor',
        'SerialNumber',
        'HardwareVersion',
        'AdditionalSoftwareVersion',
        'SoftwareVersion',
        'X_ASB_COM_Chipset',
        'lotnumber']

if len(sys.argv) > 1:
    password = sys.argv[1]
    caps = DesiredCapabilities().CHROME
    caps["marionette"] = True
    # caps["pageLoadStrategy"] = "normal"  # complete
    caps["pageLoadStrategy"] = "none"  # interactive
    driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER, desired_capabilities=caps)
    driver.get(URL)
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
    finally:
        print("founded: username")
    driver.find_element_by_id("username").send_keys('admin')
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath(r'//*[@id="loginform"]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/input').submit()
    try:
        element = WebDriverWait(driver, 60).until(EC.title_contains('Easy setup'))
    finally:
        print("founded: Title")
    driver.get(URL_INFORMATION)
    try:
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "ProductClass")))
    finally:
        print("founded: Status")
    row = []
    for key in keys:
        row.append(driver.find_element_by_id(key).text)
    # coping
    result = io.StringIO()
    w = csv.writer(result, csv.excel_tab)
    w.writerow(row)
    data = result.getvalue()
    print('Data: ' + data)
    pyperclip.copy(data)
    print("Copied to clipboard")
    print('Exiting . . .')
    driver.quit()
else:
    print("Wrong argument, please input password!")
