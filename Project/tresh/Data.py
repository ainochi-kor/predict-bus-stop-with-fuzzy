import sys
import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import unittest

class Test(unittest.TestCase):
    """ Demonstration: Get Chrome to generate fullscreen screenshot """

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=3840x2160')
        #options.add_argument('disable-gpu')
        try:
            driver = webdriver.Chrome('chromedriver_win32\chromedriver.exe', chrome_options=options)
        except:
            driver = webdriver.Chrome(
                '/home/ainochi/Desktop/project/HowToFuzzy/Project/04_BusStop_Infomation/chromedriver_linux64/chromedriver',
                chrome_options=options)

    def tearDown(self):
        self.driver.quit()

    def test_fullpage_screenshot(self):
        ''' Generate document-height screenshot '''

        url = "http://bus.busan.go.kr/busanBIMS/bus_map/map_main2.asp?menuNum=4"
        self.driver.get(url)

        time.sleep(3)

        now = datetime.datetime.now()
        if (True) :
            elem = self.driver.find_element_by_id("txtLineNum")
            elem.clear()
            elem.send_keys("68")
            self.driver.find_element_by_xpath("//*[@id=\"am_topm2_5\"]/ul/li[5]/button/img").click()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            print(soup.prettify())

            now = datetime.datetime.now()
            time.sleep(4)
            formatted = now.strftime('%Y%m%d%H%M%S')
            self.driver.get_screenshot_as_file("Bus68/"+formatted+"_BusNo68.png")
            #
            # elem.clear()
            # elem.send_keys("40")
            # self.driver.find_element_by_xpath("//*[@id=\"am_topm2_5\"]/ul/li[5]/button/img").click()
            # now = datetime.datetime.now()
            # time.sleep(4)
            # formatted = now.strftime('%Y%m%d%H%M%S')
            # self.driver.get_screenshot_as_file("Bus40/" + formatted + "_BusNo40.png")
            #
            # elem.clear()
            # elem.send_keys("138-1")
            # self.driver.find_element_by_xpath("//*[@id=\"am_topm2_5\"]/ul/li[5]/button/img").click()
            # now = datetime.datetime.now()
            # time.sleep(4)
            # formatted = now.strftime('%Y%m%d%H%M%S')
            # self.driver.get_screenshot_as_file("Bus138-1/"+formatted + "_BusNo138-1.png")
            #
            # elem.clear()
            # elem.send_keys("81")
            # self.driver.find_element_by_xpath("//*[@id=\"am_topm2_5\"]/ul/li[5]/button/img").click()
            # now = datetime.datetime.now()
            # time.sleep(4)
            # formatted = now.strftime('%Y%m%d%H%M%S')
            # self.driver.get_screenshot_as_file("Bus81/" + formatted + "_BusNo81.png")
            #
            # elem.clear()
            # elem.send_keys("17")
            # self.driver.find_element_by_xpath("//*[@id=\"am_topm2_5\"]/ul/li[5]/button/img").click()
            # now = datetime.datetime.now()
            # time.sleep(4)
            # formatted = now.strftime('%Y%m%d%H%M%S')
            # self.driver.get_screenshot_as_file("Bus17/"+formatted + "_BusNo17.png")
        else :
            time.sleep(3600)



if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])




