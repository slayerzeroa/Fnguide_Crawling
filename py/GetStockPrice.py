# -*- coding: utf-8 -*- 

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd


df_krx = fdr.StockListing('KRX')

df_fn = pd.read_csv("C:\\Users\\PC\\source\\repos\\GetStockPrice\\GetStockPrice\\csv_tb_fg_exrt_risk_i.csv", encoding='euc-kr')

code_list = []
for idx in df_fn.index:
    code = df_fn.loc[idx, '거래소코드']
    code = str(code)
    if len(code) == 2:
        code = '0000' + code
    elif len(code) == 3:
        code = '000' + code
    elif len(code) == 4:
        code = '00' + code
    elif len(code) == 5:
        code = '0' + code
    else:
        code = code
    code_list.append(code)

df_fn['market_code'] = code_list
df_fn = df_fn.sort_values(by=['거래소코드', '회계년월'], axis=0)

df_min = df_fn[['market_code', '회계년월']].groupby('market_code').min()

print(df_min)

list_min = list(df_min['회계년월'])
list_min_1 = list()
for date in list_min:
    date = str(date) + '01'
    list_min_1.append(date)
list_min = list_min_1
print(list_min)

ticker_dict = dict()
idx = 0
for ticker in df_fn['market_code']:
    ticker_dict[ticker] = list_min[idx]

print(ticker_dict)

code_list = list(df_fn['market_code'].sample(200, random_state=7))
print(code_list)

stock_price_sequence = pd.DataFrame()

forex_list = ['USD/KRW', 'JPY/KRW'] # 달러, 위안, 엔, 유로

for forex in forex_list:
    df = fdr.DataReader(symbol=forex, start='2011-12-01')
    df_close = df['Close']
    stock_price_sequence = pd.concat([stock_price_sequence, df_close], axis=1)
    print("concating...")

for code in code_list:
    df = fdr.DataReader(symbol=code, start=ticker_dict[code])
    df_close = df['Close']
    df_close.columns = [code]
    df_close = df_close.dropna(axis=0)
    stock_price_sequence = pd.concat([stock_price_sequence, df_close], axis=1, join='outer')
    print("concating...")

stock_price_sequence.columns = forex_list + code_list

stock_price_sequence.to_csv("C:\\Users\\PC\\source\\repos\\GetStockPrice\\stock_price_sequences.csv")
