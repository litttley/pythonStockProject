import pandas as pd
import numpy as np
from chinese_calendar import is_workday
from bao_stock_api import BaoStockApi, SqlAction
import datetime
import math
from eastmoneyapi.east_money_api import EastmoneyRequestbuild


def moving_average(array, n):
    # array为每日收盘价组成的数组,

    # n可以为任意正整数，按照股市习惯，一般设为5或10或20、30、60等

    mov = np.cumsum(array, dtype=float)

    mov[n:] = mov[n:] - mov[:-n]

    moving = mov[(n - 1):] / n

    return moving


# 获得距离当日前五十日的日期（周末，节假日剔除）
def days_of_fiftyone(today_date):
    cnt = 0
    prev = today_date

    while (cnt < 50):
        if is_workday(prev):
            cnt += 1
        prev -= datetime.timedelta(days=1)
    while not is_workday(prev):
        prev -= datetime.timedelta(days=1)

    return prev.strftime('%Y-%m-%d'), today_date.strftime('%Y-%m-%d')


'''
选股策略:换手率 斜率选股
'''
if __name__ == '__main__':
    # 登陆系统
    bsApi = BaoStockApi()

    if bsApi.isLogin:
        # 获取上证50成分股
        codes_code_list = SqlAction.get_codes_code_list()
        now_date_time = datetime.datetime.now() + datetime.timedelta(days=0)
        twentyone_days_ago, now_date = days_of_fiftyone(now_date_time)
        if len(codes_code_list) > 0:
            for code in codes_code_list:
                print("股票代码:%s" % code)
                #code='sh.600291'
                history_k_date_list, fields = bsApi.query_history_k_data_plus(stock_code=code,
                                                                              start_date=twentyone_days_ago,
                                                                              end_date=now_date)
                df = pd.DataFrame(history_k_date_list, columns=fields)
                df.sort_values(by='date', ascending=False, inplace=True)  # 降序排序
                df['turn'].fillna('', inplace=True)
                close_data = df['close'].astype('float')

                turn_data = df['turn'].apply(lambda x: 0 if x == '' else x).astype('float')
                volume_data = df['volume'].apply(lambda x: 0 if x == '' else x).astype('float')
                volume_data_now =volume_data.iloc[0]
                volume_data_now_1 =volume_data.iloc[1]
                now_turn_rate = turn_data.iloc[0]
                if now_turn_rate <5 or  volume_data_now/ volume_data_now_1 < 2:
                    continue

                now_price = close_data.iloc[0]  # 当前股价
                now_price_prev_1 = close_data.iloc[1]  # 前1天股价
                now_price_prev_2 = close_data.iloc[2]  # 前2天股价
                now_price_prev_3 = close_data.iloc[3]  # 前3天股价
                now_price_prev_4 = close_data.iloc[4]  # 前4天股价
                if now_price > now_price_prev_1 :
                    pass
                else:
                    continue

                mad_5 = np.mean(close_data[:5]).round(2)
                print("5日均线%s" % mad_5)
                mad_10 = np.mean(close_data[:10]).round(2)
                print("10日均线%s" % mad_5)
                mad_20 = np.mean(close_data[:20]).round(2)
                print("20日均线%s" % mad_5)

                mad_5_pre_1 = np.mean(close_data[1:6]).round(2)
                mad_10_pre_1 = np.mean(close_data[1:11]).round(2)
                mad_20_pre_1 = np.mean(close_data[1:21]).round(2)
                print("前一个5日均线%s" % mad_5_pre_1)
                print("前一个10日均线%s" % mad_10_pre_1)
                print("前一个20日均线%s" % mad_20_pre_1)



                mad_5_angle = round(math.atan((mad_5 / mad_5_pre_1 - 1) * 100) * 180 / 3.1415926, 2)
                mad_10_angle = round(math.atan((mad_10 / mad_10_pre_1 - 1) * 100) * 180 / 3.1415926, 2)
                mad_20_angle = round(math.atan((mad_20 / mad_20_pre_1 - 1) * 100) * 180 / 3.1415926, 2)

                mad_5_pre_2 = np.mean(close_data[2:7]).round(2)
                mad_10_pre_2 = np.mean(close_data[2:12]).round(2)
                mad_20_pre_2 = np.mean(close_data[2:22]).round(2)
                print("前两个5日均线%s" % mad_5_pre_2)
                print("前两个10日均线%s" % mad_10_pre_2)
                print("前两个20日均线%s" % mad_20_pre_2)


                first_df = df.head(1)
                first_array = np.array(first_df).tolist()

                #if mad_5_angle > mad_10_angle > mad_20_angle > 30:
                if mad_5_angle > mad_10_angle > mad_20_angle > 30:
                    SqlAction.insert_turn_rate(first_array, mad_5, mad_10, mad_20, mad_5_angle,
                                               mad_10_angle, mad_20_angle)
