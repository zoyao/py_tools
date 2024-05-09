from selenium import webdriver
from requests_html import HTMLSession


driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chrome.exe')
url = 'http://www.baidu.com'
driver.maximize_window()
driver.get(url)

pass