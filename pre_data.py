import os
import pandas as pd
from datetime import date, datetime


# 民國轉西元
# eg. 106/01/01 => 2017/01/01
def date_convert(strDate):
    arydate = strDate.split("/")
    return date(int(arydate[0]) + 1911, int(arydate[1]), int(arydate[2])).strftime('%Y/%m/%d')


# 資料整理：每5秒委託成交統計、每5秒指數盤後統計
def five_min_data(param1, param2):
    for path, dirs, files in os.walk(os.path.join(os.getcwd(), param1 + "/")):
        yyyymm = [x[:6] for x in files if x[-4:] == ".csv"]
        yyyymm = set(yyyymm)
        for ym in yyyymm:
            df_ym = pd.DataFrame()
            for f in [x for x in files if x[:6] == ym]:
                try:
                    df_temp = pd.read_csv(os.path.join(path, f), encoding="BIG5", skiprows=1)
                    # drop empty rows
                    df_temp = df_temp[pd.notnull(df_temp[param2])]
                    df_temp.insert(0, "日期", datetime.strftime(datetime.strptime(f[:8], "%Y%m%d"), "%Y/%m/%d"))
                    ####################################################################################################
                    # df_temp = df_temp[df_temp['時間'] == "13:30:00"]
                    df_temp = df_temp.assign(TEMP=df_temp['時間'])
                    df_temp['TEMP'] = df_temp['TEMP'].apply(
                        lambda x: datetime.strptime(x.replace("=", "").replace("\"", ""), '%H:%M:%S'))
                    df_temp['TEMP'] = df_temp['TEMP'].apply(lambda x: datetime.strftime(x, '%S'))
                    df_temp = df_temp[df_temp['TEMP'] == '00']
                    del df_temp['TEMP']
                    ####################################################################################################
                    df_ym = pd.concat([df_ym, df_temp])
                except pd.errors.EmptyDataError as e:
                    pass
                finally:
                    pass
            # drop empty columns
            df_ym = df_ym.dropna(axis=1, how='all')
            # sort by date & time
            df_ym['時間'] = df_ym['時間'].apply(
                lambda x: datetime.strptime(x.replace("=", "").replace("\"", ""), '%H:%M:%S'))
            df_ym = df_ym.sort_values(["日期", "時間"])
            df_ym['時間'] = df_ym['時間'].apply(lambda x: datetime.strftime(x, '%H:%M:%S'))
            # output to csv
            output_path = os.path.join(os.getcwd(), "all_data/" + param1 + "_" + ym + ".csv")
            df_ym.to_csv(path_or_buf=output_path, encoding="BIG5", index=False)


# FMTQIK 每日市場成交資訊
df_FMTQIK = pd.DataFrame()
for path, dirs, files in os.walk(os.path.join(os.getcwd(), "FMTQIK/")):
    for f in files:
        if f.endswith('.csv'):
            df_temp = pd.read_csv(os.path.join(path, f), encoding="BIG5", skiprows=1)
            df_FMTQIK = pd.concat([df_FMTQIK, df_temp])
# drop empty columns
df_FMTQIK = df_FMTQIK.dropna(axis=1, how='all')
# drop empty rows
df_FMTQIK = df_FMTQIK[pd.notnull(df_FMTQIK['成交股數'])]
# date convert
df_FMTQIK['日期'] = [date_convert(x) for x in df_FMTQIK['日期']]
# sort by date
df_FMTQIK = df_FMTQIK.sort_values("日期")
# output to csv
output_path = os.path.join(os.getcwd(), "all_data/FMTQIK.csv")
df_FMTQIK.to_csv(path_or_buf=output_path, encoding="BIG5", index=False)

# MI_5MINS 每5秒委託成交統計
five_min_data("MI_5MINS", '累積委託買進筆數')

# MI_5MINS_INDEX 每5秒指數盤後統計
five_min_data("MI_5MINS_INDEX", '發行量加權股價指數')

# 資料比對
df_FMTQIK = pd.read_csv(os.path.join(os.getcwd(), "all_data/FMTQIK.csv"), encoding="BIG5")
print("=====df_FMTQIK=====")
print(df_FMTQIK.shape)
print(df_FMTQIK.min(0, '日期')['日期'])
print(df_FMTQIK.max(0, '日期')['日期'])

df_MI_5MINS = pd.DataFrame()
df_MI_5MINS_INDEX = pd.DataFrame()
for path, dirs, files in os.walk(os.path.join(os.getcwd(), "all_data/")):
    for f in files:
        if f.endswith('.csv'):
            df_temp = pd.read_csv(os.path.join(path, f), encoding="BIG5")
            if f[:14] == "MI_5MINS_INDEX":
                df_MI_5MINS_INDEX = pd.concat([df_MI_5MINS_INDEX, df_temp[df_temp['時間'] == "13:30:00"]])
            elif f[:8] == "MI_5MINS":
                df_MI_5MINS = pd.concat([df_MI_5MINS, df_temp[df_temp['時間'] == "13:30:00"]])
print("=====df_MI_5MINS=====")
print(df_MI_5MINS.shape)
print(df_MI_5MINS.min(0, '日期')['日期'])
print(df_MI_5MINS.max(0, '日期')['日期'])
print("=====df_MI_5MINS_INDEX=====")
print(df_MI_5MINS_INDEX.shape)
print(df_MI_5MINS_INDEX.min(0, '日期')['日期'])
print(df_MI_5MINS_INDEX.max(0, '日期')['日期'])

df_check = pd.merge(df_FMTQIK, df_MI_5MINS, how='left', on="日期")
df_check = pd.merge(df_check, df_MI_5MINS_INDEX, how='left', on="日期")
print("=====df_check=====")
print("----時間----")
print(df_check[df_check['時間_x'] != df_check['時間_y']])
print("----發行量加權股價指數----")
print(df_check[df_check['發行量加權股價指數_x'] != df_check['發行量加權股價指數_y']])
