# Author : Daemyeong Yoo
# This is a checking fnguide's csv file python program
# We want to check the number of companys
# pip install dart-fss


import dart_fss as dart
import csv
import pandas as pd
from dart_fss.errors import NotFoundConsolidated

df_fn = pd.read_csv('./data.csv', encoding='euc-kr')


# 거래소코드 전처리
code_list = []
for idx in df_fn.index:
    code = df_fn.loc[idx, '거래소코드']
    code = str(code)
    if len(code) == 2:
        code = '0000' + str(code)
    elif len(code) == 3:
        code = '000' + str(code)
    elif len(code) == 4:
        code = '00' + str(code)
    elif len(code) == 5:
        code = '0' + str(code)
    else:
        code = str(code)
    code_list.append(code)

df_fn['market_code'] = code_list
# sort
# 거래소코드, 회계년월 기준 오름차순 정리
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

# Open-api 키 설정
api_key = '1e3c253c07d1b1600ce7cf5d6beb756ea7946a1b'
dart.set_api_key(api_key=api_key)

print(len(code_list))
# 재무제표 받아오기
# 연결재무제표 > 개별재무제표 (try-except문으로 처리)
company_list = dart.get_corp_list()
index = 0
for code in code_list:
    company = company_list.find_by_stock_code(code)
    print(code)
    try:
        fs = company.extract_fs(bgn_de=ticker_dict[code], separate=False, report_tp=['quarter']) # 연결재무제표추출
        index+=1
        fs.save(filename=f'{code}.xlsx', path="./fs/")
    except:
        try:
            fs = company.extract_fs(bgn_de=ticker_dict[code], separate=True, report_tp=['quarter'])  # 개별제무재표추출
            index+=1
            fs.save(filename=f'{code}.xlsx', path="./fs/")
        except:
            pass
