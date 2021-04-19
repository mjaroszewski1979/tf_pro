import pandas as pd
import pandas_datareader.data as pdr
import datetime

def get_trend(symbol, start = datetime.datetime(2020, 1, 1), end = datetime.datetime.now()):
    df = pdr.DataReader(symbol, 'fred', start, end)
    if df[symbol][-1] > df[symbol][-252]:
        return 'UPTREND'
    else:
        return 'DOWNTREND'

data=[{'name':'S&P 500'}, {'name':'GOLD'}, {'name':'BITCOIN'}]
data_pro = [{'name':'S&P 500'}, {'name':'NASDAQ'}, {'name':'DOW JONES'}, {'name':'NIKKEI'}, {'name':'GOLD'}, {'name':'SILVER'}, 
            {'name':'BITCOIN'}, {'name':'LITECOIN'}, {'name':'ETHEREUM'}, {'name':'US DOLLAR'}, {'name':'JP YEN'}, {'name':'CH FRANC'}, {'name':'CA DOLLAR'}]

markets = {
    'S&P 500' : 'SP500',
    'GOLD' : 'GOLDAMGBD228NLBM',
    'BITCOIN' : 'CBBTCUSD'
    }  

markets_pro = {
    'S&P 500' : 'SP500',
    'DOW JONES' : 'DJIA',
    'NASDAQ' : 'NASDAQ100',
    'NIKKEI' : 'NIKKEI225',
    'GOLD' : 'GOLDAMGBD228NLBM',
    'SILVER' : 'SLVPRUSD',
    'US DOLLAR' : 'DTWEXBGS',
    'JP YEN' : 'DEXJPUS',
    'CH FRANC' : 'DEXSZUS',
    'CA DOLLAR' : 'DEXCAUS',
    'BITCOIN' : 'CBBTCUSD',
    'LITECOIN' : 'CBLTCUSD',
    'ETHEREUM' : 'CBETHUSD'
    }   