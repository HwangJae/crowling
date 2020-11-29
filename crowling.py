# parser.py
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import urllib.request
import os
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve

def sleep(sec):
  time.sleep(sec)


class Crowling:
  def __init__(self):
    self.driver = webdriver.Chrome(".\chromedriver.exe")

  def goPage(self, url):
    # driver.get('https://www.instagram.com/')
    self.driver.get(url)
    sleep(3)

  def getCurHtml(self):
    html = self.driver.page_source
    soup = bs(html, "html.parser")  # beautifulSoup 연동
    return soup

  def search(self, keyword):
    searchInput = self.driver.find_elements_by_css_selector(self.searchTag)[0]
    searchInput.send_keys(keyword)
    sleep(1)
    searchInput.send_keys(Keys.RETURN)
    sleep(1)
    searchInput.send_keys(Keys.RETURN)
    sleep(3)

  def scrollDown(self):
    curScrollPos = "document.documentElement.scrollTop"
    self.driver.execute_script(f"window.scrollTo(0, {curScrollPos}+500)")

  def writeImgFile(self,keyword,filename,src):
    folderName = 'food/{keyword}'
    isExistFolder = os.path.isdir(folderName)
    if isExistFolder:
      os.mkdir(folderName)
    urlretrieve(src,f'{folderName}/{keyword}_{filename}.png') #request로 받을려고 했는데 안되서 이걸로 함

class CrowlingGoogle(Crowling):
  # def __init__(self): 
  #   super().__init__()

  def strUrl(self,keyword):
    return f"https://www.google.com/search?q={keyword}&sxsrf=ALeKk00DD1HmfNS4eOvuXsqTxTAsiuTzyg:1606650106650&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj4g4qH1qftAhU1K6YKHTEWCIoQ_AUoAXoECAYQAw&cshid=1606650111833509&biw=1020&bih=786"

  def convertImgTag(self):
    imgTag = f"div > div > a > div > img"
    return imgTag

  def init(self):
    pass

  def getImgSrc(self, index):
    soup = super().getCurHtml()
    imgTag = soup.select(self.convertImgTag())[index]
    return imgTag

  def crowling(self, keyword, maxNum):
    super().goPage(self.strUrl(keyword))
    
    for index in range(1, maxNum):
      imgTag = self.getImgSrc(index)
      if imgTag == None: return

      if "src" in imgTag.attrs:  # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}
        src = imgTag.attrs["src"]
        super().writeImgFile(keyword,index,src)
      super().scrollDown()


# class CrowlingInsta(Crowling):
#   def __init__(self):
#     self.idTag = "#loginForm > div > div > div > label > input"
#     self.pwTag = "#loginForm > div > div > div > label > input"
#     self.searchTag = "#react-root > section > nav > div > div > div > div > input"

#   def strImgTag(self, index):
#     imgTag = f"div > div > div:nth-child({index/3+1}) > div:nth-child({index%3+1}) > a > div > div > img"
#     return imgTag

#   def getImgSrc(self, index):
#     imgTag = self.soup.select(strImgTag(index))[0]

#   def login(self, id, pw):
#     idInput = self.driver.find_elements_by_css_selector(self.idTag)[0]
#     idInput.send_keys(id)
#     sleep(1)
#     passwordInput = self.driver.find_elements_by_css_selector(self.pwTag)[1]
#     passwordInput.send_keys(pw)
#     sleep(1)
#     passwordInput.submit()

#   def init(self):
#     pass

#   def process(self, url, maxNum):

#     srcList = []
#     for index in range(1, maxNum):
#       imgTag = getImgSrc(index)
#       if (
#         "src" in imgTag.attrs
#       ):  # 내부에 있는 항목들을 리스트로 가져옵니다 ex) {u'href': u'//www.wikimediafoundation.org/'}
#         src = imgTag.attrs["src"]
#         srcList.append(src)
#         print(src)
#       super().scrollDown()
#     return srcList





# bot = CrowlingGoogle()
# srcList = bot.crowling("뿌링클", 1000)
# print(srcList)

# id =
# password =


# searchInput = driver.find_elements_by_css_selector('#react-root > section > nav > div > div > div > div > input')[0]
# searchInput.send_keys("#bhc 뿌링클")
# time.sleep(1)
# searchInput.send_keys(Keys.RETURN)
# time.sleep(1)
# searchInput.send_keys(Keys.RETURN)
# time.sleep(3)

# html = driver.page_source
# #beautifulSoup 연동
# soup = bs(html, 'html.parser')
# imgTags = soup.select('div > div > div:nth-child(1) > div:nth-child(2) > a > div > div > img')


# print('갯수 :' + len(imgTags))
# for imgTag in imgTags:
#     print(imgTag['src'] + '\n')


# first_page = s.get('https://www.instagram.com/')
# html = first_page.text
# soup = bs(html, 'html.parser')
# # csrf = soup.find('input', {'name': '_csrf'}) # input태그 중에서 name이 _csrf인 것을 찾습니다.
# # print(csrf['value']) # 위에서 찾은 태그의 value를 가져옵니다.

# # 이제 LOGIN_INFO에 csrf값을 넣어줍시다.
# # (p.s.)Python3에서 두 dict를 합치는 방법은 {**dict1, **dict2} 으로 dict들을 unpacking하는 것입니다.
# # LOGIN_INFO = {**LOGIN_INFO, **{'_csrf': csrf['value']}}
# print(LOGIN_INFO)
