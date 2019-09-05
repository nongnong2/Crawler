import requests
from bs4 import BeautifulSoup
import re
import csv
import urllib.parse as urlparse
from selenium import webdriver

leakforum_id = 'rnjswldyd133@gmail.com'
leakforum_password = 'rkawkxkd##1'

class LeakedForumsSpider:
  def __init__(self):
    self.stat_url = "https://leakforums.co/index.php?resources/" #resourecs페이지로 바로 이동
    self.csvfile = open('LeakedForums_datavases_category_hotlist.csv', 'w', encoding='utf-8', newline='')
    self.filewriter = csv.writer(self.csvfile)
  
  def __del__(self):
    self.csvfile.close()

  def LoginNparse(self, leakforum_id, leakforum_password):
    #로그인 하는 부분
    driver = webdriver.Chrome(r'C:\chromedriver') #chromedriver를 저장한 위치를 넣어주세요
    driver.implicitly_wait(3)
    start_url = "https://leakforums.co/index.php?resources/" #Resourecs 페이지로 바로 접근
    leakforum_id = leakforum_id
    leakforum_password = leakforum_password
    driver.get(start_url)
    driver.find_element_by_name('login').send_keys(leakforum_id)#ID를 넣어줍니다.
    driver.find_element_by_name('password').send_keys(leakforum_password)#password를 넣어줍니다.
    driver.find_element_by_xpath('//*[@id="top"]/div[4]/div/div/div/div/div/div[2]/form/div[1]/dl/dd/div/div[2]/button').click()#로그인 버튼을 눌러줍니다.

    while True:
      html = driver.page_source
      bs_obj = BeautifulSoup(html, 'html.parser')
      post_list = bs_obj.select('div.structItem')

      for post in post_list:
        try:
          title = post.select_one('div.structItem-title > a:nth-child(2)').text.strip()
        except: #타이틀만 있는 경우도 있고 데이터 유형도 같이 있는 경우도 있어 예외처리 했습니다!
          title = post.select_one('div.structItem-title > a').text.strip()  
          continue
        date = post.select_one('dl.structItem-metaItem--lastUpdate').text.strip().replace('\n','').replace(',',' ')
        star_rate = post.select_one('span.ratingStars--larger').text.strip()
        download_rate = post.select_one('dl.structItem-metaItem--downloads').text.strip().replace('\n', '')
        try:
          data_type = post.select_one('div.structItem-title > a.labelLink > span').text.strip()
        except:
          data_type = "none"
          continue

        Date = re.sub(r'Updated','',date)
        r_Date = re.sub(r'at.*','',Date)
        Star_rate = re.sub(r' star\(s\)','',star_rate)
        Download_rate = re.sub(r'Downloads','',download_rate)  
        self.filewriter.writerow([title, r_Date, Star_rate, Download_rate, data_type])

      if not bs_obj.select_one('a.pageNav-jump--next'):
        break
      else:
        driver.find_element_by_class_name('pageNav-jump--next').click()

if __name__ == "__main__":
  spider = LeakedForumsSpider()
  spider.LoginNparse('rnjswldyd133@gmail.com','rkawkxkd##1')

       

    
 