import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def crawl(url):
    data = requests.get(url)
    print(data)
    return data.content

def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text

    aTag = tds[1].find("a")
    href = aTag["href"]
    name = aTag.text

    nowPrice = tds[2].text
    Volume= tds[6].text #거래량
    TotalPrice = tds[7].text #시가총액
    EPS = tds[8].text #주당순이익
    OPR = tds[9].text #Operating profit increase(영업이익 증가율)
    PER = tds[10].text 
    ROE = tds[11].text
    EPS_num = int(EPS.replace(",",""))
    return {"rank":rank, "name":name, "code":href[20:],
            "nowPrice":nowPrice, "거래량":Volume,"TotalPrice":TotalPrice,
            "EPS":EPS,"영업이익증가율":OPR, "PER":PER,"ROE":ROE, "EPS*ROE":EPS_num*float(ROE), "EPS *10":EPS_num * 10}

def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class":"box_type_l"})
    type_2 = box_type_l.find("table", {"class":"type_2"})
    t_body = type_2.find("tbody")
    trs = t_body.findAll("tr")
    StockInfos = []
    for tr in trs:
        try:
            StockInfo = getStockInfo(tr)
            StockInfos.append(StockInfo)
        except Exception as e:
            print("error")
            pass
    return StockInfos

def getSiseMarketSum(sosok, page):
    driver = webdriver.Chrome(r'C:\chromedriver')
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok={}&page={}".format(sosok, page)
    #외국인 비율, 상장주식수,  주당순이익, 영업이익 증가율 눌러야함
    driver.get(url) 
    driver.implicitly_wait(2) #페이지 접속 대기
    driver.find_element_by_id('option15').click() #외국인 비율
    driver.find_element_by_id('option21').click() #상장주식수
    driver.find_element_by_id('option11').click() # 영업이익증가율
    driver.find_element_by_id('option23').click() #주당순이익 버튼 
    driver.find_element_by_xpath('//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]').click() #적용버튼 클릭 
    driver.implicitly_wait(2) #페이지 대기 
    
    window = 'me_layers'
    driver.switch_to_window #iframe 요소 가져오기 
    pageString = driver.page_source
    List = parse(pageString)
    return List 

def WriteCsv(data):
    with open('Korea_Stock_Info.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['순위', '이름', '코드', '현재가', '거래량', '시가총액', 'EPS', '영업이익증가율', 'PER', 'ROE', '적정주가(EPS*ROE)', 'EPS * 10'])
        for row in data:
            csv_out.writerow(row.values())

if __name__ == "__main__":
    Chose_market = int(input("코스피는 0, 코스닥은 1: "))
    if Chose_market == 0:
        result = []
        for page in range(1, 11): #500개 할꺼면 10페이지
            List = getSiseMarketSum(0, page) # 0이 코스피, 1인 코스닥 
            result += List
        WriteCsv(result)

    else:
        result = []
        for page in range(1, 11): #500개 할꺼면 10페이지
            List = getSiseMarketSum(1, page) # 0이 코스피, 1인 코스닥 
            result += List
        WriteCsv(result)
    print("정리 완료!")
