import requests
from bs4 import BeautifulSoup
# bitcoin은 가치저장의 수단으로 생각, 금의 지위를 어느정도 대체
# 단위 kg, 달러

def GetBitInfo():
    headers = {'User-Agent': 'Mozilla/5.0'}
    bit_url = "https://coinmarketcap.com/currencies/bitcoin/" #forbidden뜸
    req = requests.get(bit_url, headers=headers)
    html = req.content
    soup = BeautifulSoup(html, 'lxml')

    bit_quantity = soup.select("#__next > div > div.sc-fzqARJ.eLpUJW.cmc-body-wrapper > div > div.sc-AxhCb.jGVDnv.container > div.sc-AxhCb.bYwLMj.container___lbFzk > div.sc-AxhCb.iOyrqq.statsSection___2aZ29 > div.hide___2JmAL.statsContainer___2uXZW > div.statsSupplyBlock___ST_Wb > div.sc-AxhCb.bSKmgr > div.statsValue___2iaoZ")[0].text
    bq1 = bit_quantity.replace(',','')
    bq2 = float(bq1.replace(' BTC',''))

    bit_price = soup.select("#__next > div > div.sc-fzqARJ.eLpUJW.cmc-body-wrapper > div > div.sc-AxhCb.jGVDnv.container > div.sc-AxhCb.bYwLMj.container___lbFzk > div.sc-AxhCb.bYwLMj.priceSection___3kA4m > div.sc-AxhCb.bYwLMj.priceTitle___1cXUG > div")[0].text
    bp1 = bit_price.replace('$','')
    bp2 = float(bp1.replace(',',''))
    return(bq2, bp2)

def Cacluate(bit_quantity, bit_price):
    # gold_quantity = int(input("금 kg양은?: "))
    gold_quantity = 201296000
    gold_price = float(input("금 1kg당 달러: ")) 
    # replace_ratio = int(input("비트코인이 금 자산 몇퍼센트가 될까?: "))/100 10%가정
    replace_ratio = 0.1

    gold_value = gold_quantity * gold_price
    bit_value = gold_value * replace_ratio / bit_quantity
    print("비트코인 가치는 ", bit_value, "달러")
    print("비트코인 현재 가격은 ",bit_price, "달러")

    if bit_price > bit_value:
        print("현재",bit_price - bit_value, " 만큼 과평가입니다.")

    else:
        print("현재" ,bit_price - bit_value, "만큼 저평가입니다.") 

if __name__ == "__main__":
    bit_info = GetBitInfo()
    bit_quantity = bit_info[0]
    bit_price = bit_info[1]
    Cacluate(bit_quantity, bit_price)

