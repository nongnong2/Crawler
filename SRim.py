#S-RIM 계산적용
#1. 자본총계(지배)
#2. 한국신용평가 홈페이지 BBB-등급
#3. 3년치 ROE
#4. 유통 주식수 

#주의! 가중평균 ROE 값이 회사채 수익률(할인률) 보다 낮으면 투자 가치가 없음
import csv
import requests
from bs4 import BeautifulSoup

def getData(code):
    url = "https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode={}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN=".format(code)
    req = requests.get(url)
    html = req.content
    soup = BeautifulSoup(html, 'lxml')
    high_D_A = soup.select("#highlight_D_A > table > tbody > tr > td")
    
    Equity_capital = high_D_A[74].text #최근 자기자본지분
    Equity_capital_num = int(Equity_capital.replace(',','')) * 100000000

    ROE_3 = float(high_D_A[136].text) #ROE3
    ROE_2 = float(high_D_A[137].text) #ROE2
    ROE_1 = float(high_D_A[138].text) #ROE1
    AvRoe = (ROE_1 + ROE_2 + ROE_3)/3 #가중평균 ROE 3년치 

    Stock_equity = high_D_A[186].text #발행주식수
    Stock_equity_num = int(Stock_equity.replace(',','')) * 1000

    Treasury_stock = soup.select('#svdMainGrid5 > table > tbody > tr > td')[17].text #자사주
    if Treasury_stock == '\xa0':
        Treasury_stock_num = int(0)
    else:    
        Treasury_stock_num = int(Treasury_stock.replace(',',''))
    
    Floating_stock_num = Stock_equity_num - Treasury_stock_num

    StockPrice = soup.select_one('#svdMainChartTxt11').text
    StockName = soup.select_one('#giName').text
    return{"StockName":StockName, "StockPrice":StockPrice, "Equity_capital":Equity_capital_num,"AvRoe":AvRoe,"Floating_Stock":Floating_stock_num}
    
def getDiscountRate():
    url = 'https://www.kisrating.com/ratingsStatistics/statics_spread.do'
    req = requests.get(url)
    html = req.content
    soup = BeautifulSoup(html, 'lxml')
    DiscountRate_5 = soup.select('#con_tab1 > div.table_ty1 > table > tbody > tr > td')[98].text #BBB- 5년 금리 
    return(float(DiscountRate_5))

def getSrim(Equity_capital_num, Discount_rate, AvRoe, Floating_stock_num):
    E_profit = Equity_capital_num * (AvRoe - Discount_rate) #초과이익 
    rates = [1, 0.9, 0.8, 0.7, 0.6, 0.5] #지속 성장 ~ 초과이익 50%하락 까지 
    results = []
    for rate in rates:
        denominator_SRim = Equity_capital_num + (E_profit * rate)/Discount_rate #S-rim 분모값
        S_Rim = denominator_SRim/Floating_stock_num    
        results.append(S_Rim)
    return(results)

if __name__ == "__main__":
    DiscountRate = getDiscountRate()
    f = open('Kospi_SRim.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(['이름', '종가', '지배주주지분', '3년 평균 ROE', '유동주식수', '지속성장', '초과이익 10% 감소', '20% 감소', '30% 감소', '40% 감소'])

    with open("./KospiCode.txt", encoding='utf-8') as f:
        for line in f:
            code = "A" + line.rstrip('\n')
            try:
                Datas = getData(code)
                output = getSrim(Datas['Equity_capital'],DiscountRate,Datas['AvRoe'],Datas['Floating_Stock'])
                results = [Datas['StockName'], Datas['StockPrice'],Datas['Equity_capital'], Datas['AvRoe'], Datas['Floating_Stock'], output[0], output[1], output[2], output[3],output[4]]
                f = open('Kospi_SRim.csv', 'a+', newline='')
                wr = csv.writer(f)
                wr.writerow(results)
                f.close()
            except:
                print(code, "에러 발생!")
    print("할인율을", DiscountRate, " 입니다!")
        
        

