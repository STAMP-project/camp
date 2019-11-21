import logging
import unittest
import os
import HtmlTestRunner
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.basicConfig(filename="DEBUG.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class SeleniumTest(unittest.TestCase):

    def setUp(self):
        self.chrome = webdriver.Remote(
            command_executor="http://hub:4444/wd/hub",
            desired_capabilities={
                "browserName": os.environ["BROWSERNAME"],
                "platform": os.environ["PLATFORM"],
                "javascriptEnabled": os.environ["JAVASCRIPTENABLED"],
                "maxInstances":os.environ["MAXINSTANCES"],
                "cssSelectorEnabled":os.environ["CSSSELECTORSENABLED"],
                "browserConnectionEnabled":os.environ["BROWSERCONNECTIONENABLED"]})
        
        self.chrome.implicitly_wait(20)
        self.chrome.set_page_load_timeout(20)
        self.chrome.maximize_window()

    def test1_navigate_weather(self):
        elements_urls = []
        self.chrome.get("http://web:82/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[0]/li[0]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn("http://localhost/dashboard/map/weather/", self.chrome.get(i))
        print("Test1 pass !!")
        self.chrome.close()

    def test2_navigate_realTimeBusData(self):
        elements_urls = []
        self.chrome.implicitly_wait(20)
        self.chrome.get("http://web:82/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[1]/li[1]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn("http://localhost/dashboard/map/bus/", self.chrome.get(i))
        print("Test2 pass !!")
        self.chrome.close()

    def test3_navigate_busStation(self):
        elements_urls = []
        self.chrome.implicitly_wait(20)
        self.chrome.get("http://web:82/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[2]/li[2]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn("http://localhost/dashboard/map/cycle/", self.chrome.get(i))      
        print("Test3 pass !!")
        self.chrome.close()

    def test4_heatMap(self):
        elements_urls = []
        self.chrome.implicitly_wait(20)
        self.chrome.get("http://web:82/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[3]/li[3]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn("http://localhost/dashboard/map/heatmap/", self.chrome.get(i))
        print("Test4 pass !!")
        self.chrome.close()

    def test5_vehicule_parking(self):
        elements_urls = []
        self.chrome.implicitly_wait(20)
        self.chrome.get("http://web:82/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[4]/li[4]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn('http://localhost/dashboard/map/parking/', self.chrome.get(i))      
        print("Test5 pass !!")
        self.chrome.close()

    def test6_analysis(self):
        elements_urls = []
        self.chrome.implicitly_wait(20)
        self.chrome.get("http://localhost/dashboard/")
        elements = self.chrome.find_elements_by_xpath(
            "//div[contains(@class,'collapse navbar-collapse')]/ul[5]/li[5]")
        for i in elements:
            elements_urls.append(i.get_attribute('href'))
            self.assertIn('http://localhost/dashboard/map/parking/', self.chrome.get(i))
        print("Test6 pass !!")
        self.chrome.close()

    def tearDown(self):
        self.chrome.quit()

if __name__=='__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="selenium_test_report"))
