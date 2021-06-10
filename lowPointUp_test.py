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

def before_day(today_date):

    prev = today_date+ datetime.timedelta(days = -1)

    while  not is_workday(prev):#  不是工作日
        prev = prev + datetime.timedelta(days = -1)

    while is_workday(prev) :# 是工作日
        return prev






'''
选股策略:求出当近1个月最低点上浮4% 8% 10%的股票
'''
if __name__ == '__main__':
    #yesterday = before_day(datetime.date(2021, 5, 24))

    # 登陆系统
    bsApi = BaoStockApi()

    if bsApi.isLogin:
        # 获取上证50成分股
        codes_code_list = SqlAction.get_codes_code_list()
        #yesterday = datetime.date.today() + datetime.timedelta(days=-1)
        yesterday = before_day(datetime.datetime.now() + datetime.timedelta(days=-1))
        twentyone_days_ago, now_date = days_of_fiftyone(yesterday)
        if len(codes_code_list) > 0:
            for code in codes_code_list:
                try:
                    history_k_date_list, fields = bsApi.query_history_k_data_plus(stock_code=code,
                                                                                  start_date=twentyone_days_ago,
                                                                                  end_date=now_date)
                    df = pd.DataFrame(history_k_date_list, columns=fields)
                    df.sort_values(by='date', ascending=False, inplace=True)  # 降序排序

                    close_data = df['close'].astype('float')
                    low_close_price = close_data.min(skipna=True)

                    low_close_price_4 = round(low_close_price * 1.04,2)
                    low_close_price_8 = round(low_close_price * 1.08,2)
                    low_close_price_10 = round(low_close_price * 1.1,2)

                    now_price = close_data.iloc[0]
                    print("当前股票:%s 收盘价:%s,50日最低价%s" % (code,now_price,low_close_price))



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
                    print("5日均线角度%s" % mad_5_angle)
                    print("10日均线角度%s" % mad_10_angle)
                    print("20日均线角度%s" % mad_20_angle)
                    mad_5_pre_2 = np.mean(close_data[2:7]).round(2)
                    mad_10_pre_2 = np.mean(close_data[2:12]).round(2)
                    mad_20_pre_2 = np.mean(close_data[2:22]).round(2)
                    print("前两个5日均线%s" % mad_5_pre_2)
                    print("前两个10日均线%s" % mad_10_pre_2)
                    print("前两个20日均线%s" % mad_20_pre_2)

                    first_df = df.head(1)
                    first_array = np.array(first_df).tolist()

                    if now_price <= low_close_price_4 and mad_5 / mad_20 > 1 and mad_5_pre_1 / mad_20_pre_1 < 1 and mad_5_angle >=30 and  mad_20_angle >= 10:

                        print("low_close_price_4:%s" % low_close_price_4)
                        SqlAction.insert_low_point_up(first_array, low_close_price_4, '', '')
                    elif low_close_price_4 < now_price <= low_close_price_8 and mad_5 / mad_20 > 1 and mad_5_pre_1 / mad_20_pre_1 < 1  and mad_5_angle >=30 and  mad_20_angle >= 10:
                        print("low_close_price_4:%s" % low_close_price_8)
                        SqlAction.insert_low_point_up(first_array, '', low_close_price_8, '')
                    elif low_close_price_8 < now_price <= low_close_price_10 and mad_5 / mad_20 > 1 and mad_5_pre_1 / mad_20_pre_1 < 1 and mad_5_angle >=30 and  mad_20_angle >= 10:
                        print("low_close_price_4:%s" % low_close_price_10)
                        SqlAction.insert_low_point_up(first_array, '', '', low_close_price_10)
                    else:
                        pass
                except Exception as e:
                    print("错误股票:%s" % code)

