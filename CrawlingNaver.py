import codecs
import datetime
import os
import time
import webbrowser
from urllib.parse import quote_plus
from urllib.request import urlopen

# import matplotlib
# import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
# from matplotlib import font_manager, rc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class naverCrawling:

    def runCrawling(self, searchKeyword, osType='windows'):

        # 여기부터 다른 코드
        baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
        searchUrl = searchKeyword
        url = baseUrl + searchUrl

        options = Options()
        # //// 이 구문을 실행시키면 window 화면에 실행 없이 Background에서 실행된다.
        options.headless = True
        if osType == 'windows':
            browser = webdriver.Chrome(".\chromedriver.exe")
        else:
            browser = webdriver.Chrome('chromedriver')  # 맥사용자를 위한 코드
        # browser = webdriver.Chrome(".\chromedriver.exe") # windows 사용자를 위한 코드

        browser.implicitly_wait(0.2)  # 1초 휴식

        print(url)
        browser.get(url)
        time.sleep(0.5)

        # 스크롤 내리는 코드
        print('scrolling')
        last_page_height = browser.execute_script(
            "return document.documentElement.scrollHeight")
        for b in range(2):
            for a in range(10):
                browser.execute_script(
                    "window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(3.0)
                new_page_height = browser.execute_script(
                    "return document.documentElement.scrollHeight")
                last_page_height = new_page_height
            time.sleep(5.0)
            # 더 보기 클릭하는 코드
            # browser.find_element_by_xpath(
            #     '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div').click()

        # fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div > div:nth-child(1) > div > div.d15Mdf.bAhLNe > div.UD7Dzf > span:nth-child(1)

        # 내용 가져오는 select문
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        img = soup.find_all(class_='_img')

        print('downloading')

        n = 1
        for i in img:
            # print(i)
            imgUrl = i['src']
            with urlopen(imgUrl) as f:
                path = './naver/' + searchUrl
                if not os.path.isdir(path):
                    os.makedirs(path)
                with open(path + '/' + searchUrl + str(n)+'.jpg', 'wb') as h:  # w - write b - binary
                    img = f.read()
                    h.write(img)
            n += 1
        print('다운로드 완료')
