import pandas as pd
import numpy as np
from chinese_calendar import is_workday
from bao_stock_api import BaoStockApi, SqlAction
import datetime
import math


def moving_average(array, n):
    # array为每日收盘价组成的数组,

    # n可以为任意正整数，按照股市习惯，一般设为5或10或20、30、60等

    mov = np.cumsum(array, dtype=float)

    mov[n:] = mov[n:] - mov[:-n]

    moving = mov[(n - 1):] / n

    return moving


# 获得距离当日前五十日的日期（周末，节假日剔除）
def days_of_twentyone(today_date):
    cnt = 0
    prev = today_date

    while (cnt < 50):
        if is_workday(prev):
            cnt += 1
        prev -= datetime.timedelta(days=1)
    while not is_workday(prev):
        prev -= datetime.timedelta(days=1)

    return prev.strftime('%Y-%m-%d'), today_date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    # 登陆系统
    bsApi = BaoStockApi()

    if bsApi.isLogin:
        # 获取上证50成分股
        codes_code_list = SqlAction.get_all_codes_code_list()
        #codes_code_list=['sz.399980']
        # data_code_list = SqlAction.get_day_data_code_list()
        #  result_code_list = list(set(codes_code_list).difference(set(data_code_list)))  # codes_code_list 有 而 data_code_list没有的 插入近两年数据
        # result_code_list_2 = list(set(codes_code_list).intersection(set(data_code_list)))  # 两者都有的，插入当天数据
        # now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        twentyone_days_ago, now_date = days_of_twentyone(datetime.datetime.now())
        if len(codes_code_list) > 0:
            for code in codes_code_list:
                try:
                    print("当前股票%s" % code)
                    history_k_date_list, fields = bsApi.query_history_k_data_plus(stock_code=code,
                                                                                  start_date=twentyone_days_ago,
                                                                                  end_date=now_date)
                    if len(history_k_date_list) <=0:
                        continue
                    df = pd.DataFrame(history_k_date_list, columns=fields)
                    df.sort_values(by='date', ascending=False, inplace=True)
                    close_data = df['close'].astype('float')
                    # mad_5 = close_data.astype('float').rolling(5).mean()
                    mad_5 = np.mean(close_data[:5]).astype(float).round(2)
                    print("5日均线%s" % mad_5)
                    mad_10 = np.mean(close_data[:10]).astype(float).round(2)
                    print("10日均线%s" % mad_5)
                    mad_20 = np.mean(close_data[:20]).astype(float).round(2)
                    print("20日均线%s" % mad_5)

                    mad_5_pre_1 = np.mean(close_data[1:6]).astype(float).round(2)
                    mad_10_pre_1 = np.mean(close_data[1:11]).astype(float).round(2)
                    mad_20_pre_1 = np.mean(close_data[1:21]).astype(float).round(2)
                    print("前一个5日均线%s" % mad_5_pre_1)
                    print("前一个10日均线%s" % mad_10_pre_1)
                    print("前一个20日均线%s" % mad_20_pre_1)

                    mad_5_angle = round(math.atan((mad_5 / mad_5_pre_1 - 1) * 100) * 180 / 3.1415926, 2)
                    mad_10_angle = round(math.atan((mad_10 / mad_10_pre_1 - 1) * 100) * 180 / 3.1415926, 2)
                    mad_20_angle = round(math.atan((mad_20 / mad_20_pre_1 - 1) * 100) * 180 / 3.1415926, 2)

                    mad_5_pre_2 = np.mean(close_data[2:7]).astype(float).round(2)
                    mad_10_pre_2 = np.mean(close_data[2:12]).astype(float).round(2)
                    mad_20_pre_2 = np.mean(close_data[2:22]).astype(float).round(2)
                    print("前两个5日均线%s" % mad_5_pre_2)
                    print("前两个10日均线%s" % mad_10_pre_2)
                    print("前两个20日均线%s" % mad_20_pre_2)

                    if mad_5 / mad_20 > 1 and mad_5_pre_1 / mad_20_pre_1 < 1:  # 上穿
                        pass
                    else:
                        continue
                    if mad_5_angle > mad_10_angle > mad_20_angle > 30:
                        first_df = df.head(1)
                        first_array = np.array(first_df).tolist()

                        # mov_mad_5 = moving_average(np.array(close_data),5)
                        SqlAction.insert_all_day_date(first_array, mad_5, mad_10, mad_20, mad_5_angle, mad_10_angle,
                                                  mad_20_angle)
                except Exception as e:
                    print(e)
