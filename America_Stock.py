import yfinance as yf

# Tickers =['AAPL', 'MSFT', 'NVDA', 'MU', 'ADBE', 'ORCL', 'INTC', 'AMD', 'CSCO', 'GOOGL', 'META', 'DIS', 'NFLX', 'AMZN','TSLA', 'KO', 'PEP', 'WMT']
Tickers =['ORCL']
def CalPER(data):
    global PER
    result = yf.Ticker(data)
    try: 
        PER = (result.info['forwardPE'] + result.info['trailingPE'])/2
    except Exception as e:
        PER = result.info['forwardPE']
        pass
    return(PER)

def CalGrowtyStock(data):
    global N_price, R_Price
    result = yf.Ticker(data)
    try:
        RPS = result.info['revenuePerShare']
        PSR = result.info['priceToSalesTrailing12Months']
        N_price = result.info['currentPrice']
        R_Price = RPS * PSR
    except Exception as e:
        print('{} error'.format(data))
        pass
    return(N_price, R_Price)

def CalBlueChipStock(data):
    global N_price, R_Price
    result = yf.Ticker(data)
    try:
        EPS = (result.info['trailingEps'] + result.info['forwardEps'])/2
        ROE = result.info['returnOnEquity']
        N_price = result.info['currentPrice']
        R_Price = EPS * ROE
    except Exception as e:
        print('{} error'.format(data))
        pass
    return(N_price, R_Price)

def Compare(Ticker, N_price, R_price):
    margin = (R_price - N_price)/ N_price * 100
    if margin <= 10:
        print('{} Not Yet! R_price is {} N_price is {} '.format(Ticker, R_Price, N_price))
    else: 
        print('{} Buy! margin is {}%! '.format(Ticker, R_price, margin * 100))

for Ticker in Tickers:
    PER = CalPER(Ticker)
    if PER >= 15:
        result = CalGrowtyStock(Ticker)
        N_price = result[0]
        R_price = result[1]
        Compare(Ticker, N_price, R_price)
    
    else :
        result = CalBlueChipStock(Ticker)
        N_price = result[0]
        R_price = result[1]
        Compare(Ticker, N_price, R_price)
