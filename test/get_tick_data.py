import datetime
import math
import time
from typing import Optional
from io import StringIO
import requests
import json
import pandas as pd
import numpy as np


class EastmoneyRequestbuild:
    def __init__(self):
        pass

    def get_stock_fen_shi_data(self, pageindex: str = '0', code: str = '', sort: str = '2', ft: str = '1') -> Optional[
        dict]:
        """
         :param pageindex: 请求页数从0开始
         :param code: 股票代码
         :param sort: 排序 1:时间正序2:时间倒序
         :param ft: 筛选大单 过滤条件 全部:1 ;ft>=100手: 2 ; ft>=200手: 3 ; ft>=500手: 4; ft>=1000手: 5; ft>=2000手: 6; ft>=5000手: 7;   ft>=10000手: 8
         :param market:  股票代码奇偶  0 : 1
         :param url: 请求地址
         :return: json数据
         """

        # pagesize 每页444条数据
        market = '0' if code[-1] == '2' else '1'
        url = 'http://push2ex.eastmoney.com/getStockFenShi?pagesize=444&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&pageindex=%s&id=%s&sort=%s&ft=%s&code=%s&market=%s&' % (
            pageindex, code, sort, ft, code[0:6], market)

        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                json_text = resp.text
                # json_text = json_text.split('(')[1].split(')')[0]
                tick_json = json.loads(json_text)
                # print(tick_json)
                return tick_json
        except Exception as e:
            print("获取分笔成交数据失败%s", e)
        return None

    def get_stock_trends2(self, stock_code: str) -> Optional[dict[str, str]]:
        # url = 'http://push2.eastmoney.com/api/qt/stock/trends2/get?fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11%2Cf12%2Cf13&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&ut=fa5fd1943c7b386f172d6893dbfba10b&ndays=1&iscr=0&iscca=0&secid=1.600029&_=1622286316980'
        url = 'http://push2.eastmoney.com/api/qt/stock/trends2/get?fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11%2Cf12%2Cf13&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&ndays=1&iscr=0&iscca=0&secid=1.{stock_code}'.format(
            stock_code=stock_code)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                json_text = resp.text
                tick_json = json.loads(json_text)
                # print(tick_json)
                return tick_json
        except Exception as e:
            print("获取分时数据失败%s", e)
        return None

    def get_stock_kline(self, minute_ktype: int, stock_code: str) -> Optional[dict[str, str]]:
        url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt={minute_ktype}&fqt=1&secid=1.{stock_code}&beg=0&end=20500000".format(
            minute_ktype=minute_ktype, stock_code=stock_code)
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                json_text = resp.text
                tick_json = json.loads(json_text)
                # print(tick_json)
                return tick_json
        except Exception as e:
            print("获取历史k线失败%s", e)
        return None


def main_1():
    build = EastmoneyRequestbuild()
    build.get_stock_kline()
    tick_json = build.get_tick_data(code='0020072')

    '''
   {'1': u'买入',
   '2': u'卖出',
'4': u'-'}
    '''
    if tick_json is None:
        raise Exception('数据加载失败')
    dt = '2021-05-28'
    ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))
    # ts = int(time.mktime((datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day,0,0,0,0,0,0)))

    data_array = tick_json['data']['data']
    count = math.ceil(tick_json['data']['tc'] / 144)  # 每页144条数据
    if count > 1:
        for x in range(1, count):
            print(x)
        for x in range(1, count):
            tick_json = build.get_tick_data(code='0020072', pageindex=x)
            array = tick_json['data']['data']
            data_array += array
    for data in data_array:
        time_str = str(data['t']).zfill(6)
        hour_timestamp = int(time_str[0:2]) * 60 * 60
        minute_timestamp = int(time_str[2:4]) * 60
        second_timestamp = int(time_str[4:6])
        timestamp = ts + hour_timestamp + minute_timestamp + second_timestamp
        data['timestamp'] = timestamp
        data['t'] = datetime.datetime.fromtimestamp(timestamp)
    df = pd.DataFrame(data_array)
    df.columns = ['time', 'price', 'vol', 'type', 'timestamp']
    df['price'] = df['price'].map(lambda x: x / 1000)
    df['type'] = df['type']
    df['timestamp'] = df['timestamp']
    df['time'] = pd.to_datetime(df['time'])
    df.set_index("timestamp")
    df.sort_values(by='timestamp', ascending=False, inplace=True)  # 降序排序
    now_timestamp = df['timestamp'].values[0:1][0]
    k_60_1 = int(time.mktime((datetime.datetime.now().year, datetime.datetime.now().month, 28, 9, 30, 0, 0, 0, 0)))
    k_60_2 = int(time.mktime((datetime.datetime.now().year, datetime.datetime.now().month, 28, 10, 30, 0, 0, 0, 0)))
    df_60_k = df[(df['timestamp'] >= k_60_1) & (df['timestamp'] <= k_60_2)]
    k_60_max = df_60_k['price'].head()
    k_60_min = df_60_k['price'].head(-1)
    # dd=time.mktime((datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 10, 30, 0, 0, 0, 0))
    # now_timestamp = timestamp.index.values[0:1][0]
    # tick_60_timestamp = now_timestamp - 60 * 60
    # tick_30_timestamp = now_timestamp - 30 * 60
    # tick_10_timestamp = now_timestamp - 10 * 60
    # tick_5_timestamp = now_timestamp - 5 * 60
    '''

    first_time = df.index.values[0:1][0]
    first_time1= datetime.datetime.fromtimestamp(int(first_time/1000000000),None).date()
    first_time  - np.timedelta64(60,'D')
    later_houer=first_time -60*60
    '''

    '''
    df_60_tick = df[(df['timestamp'] >= tick_60_timestamp) & (df['timestamp'] <= now_timestamp)]
    tick_mad_60 = np.mean(df_60_tick['price']).round(2)
    print("60分钟均值%s" %tick_mad_60)

    df_60_tick_pre = df[(df['timestamp'] >= tick_60_timestamp-60*60) & (df['timestamp'] <= tick_60_timestamp)]
    tick_mad_60_pre = np.mean(df_60_tick['price']).round(2)
    print("最近60分钟均值%s" % tick_mad_60_pre)

    df_30_tick = df[(df['timestamp'] >= tick_30_timestamp) & (df['timestamp'] <= now_timestamp)]
    tick_mad_30 = np.mean(df_30_tick['price']).round(2)
    print("最近30分钟均值%s" % tick_mad_30)

    df_10_tick = df[(df['timestamp'] >= tick_10_timestamp) & (df['timestamp'] <= now_timestamp)]
    tick_mad_10 = np.mean(df_30_tick['price']).round(2)
    print("最近10分钟均值%s" % tick_mad_10)

    df_5_tick = df[(df['timestamp'] >= tick_5_timestamp) & (df['timestamp'] <= now_timestamp)]
    tick_mad_5 = np.mean(df_5_tick['price']).round(2)
    print("最近5分钟均值%s" % tick_mad_5)

    '''


minute_k_type = {"minute_k_60": 15, "minute_k_60": 30, "minute_k_60": 60, "minute_k_60": 120}


def get_current_real_time(trend_array: list[str], k_lines: list[dict], minute_k_line: int) -> Optional[dict[str, str]]:
    s = json.dumps(trend_array)
    df = pd.read_json(s, orient='records')

    df["time"] = pd.to_datetime(df['time'], format="%Y/%m/%d %H:%M:%S")
    df["open"] = df["open"].astype("float64")
    df["close"] = df["close"].astype("float64")
    df["volume"] = df["volume"].astype("int64")
    df["amount"] = df["amount"].astype("float64")
    df["averages"] = df["averages"].astype("float64")

    df.set_index('time', inplace=True)
    df.sort_values(by='time', ascending=False, inplace=True)  # 降序排序

    range_date_array = []
    for x in range(1, int(120 / minute_k_line) + 1):
        range_time_start = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                             datetime.datetime.now().day, 9, 30, 0) + datetime.timedelta(
            minutes=minute_k_line * (x - 1))
        range_time_end = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                           datetime.datetime.now().day, 9, 30, 0) + datetime.timedelta(
            minutes=minute_k_line * x)
        range_date_array.append({"range_time_start": range_time_start, "range_time_end": range_time_end})
    print(range_date_array)

    for x in range(1, int(120 / minute_k_line) + 1):
        range_time_start = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                             datetime.datetime.now().day, 13, 0, 0) + datetime.timedelta(
            minutes=minute_k_line * (x - 1))
        range_time_end = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                           datetime.datetime.now().day, 13, 0, 0) + datetime.timedelta(
            minutes=minute_k_line * x)
        range_date_array.append({"range_time_start": range_time_start, "range_time_end": range_time_end})
    print(range_date_array)

    k_minute_close_array = []

    for time_range in range_date_array:
        try:
            range_time_start = time_range['range_time_start']
            range_time_end = time_range['range_time_end']

            df_k_minute = df[(df.index >= range_time_start) & (df.index <= range_time_end)]
            df_k_60_open_price = df_k_minute['close'].head(1)
            close = df_k_60_open_price.iloc[0]
            k_minute_close_array.append({"time_str": range_time_end.strftime("%Y-%m-%d %H:%M"), 'close': close})
        except BaseException as e:
            print("当前时间段无数据,跳过%s", range_time_end.strftime('%Y-%m-%d %H:%M'))

    k_lines.extend(k_minute_close_array)
    close_5 = [float(x['close']) for x in k_lines[-5:]]
    mad_5 = np.mean(close_5).round(2)
    print("5日均线%s" % mad_5)

    close_5_pre = [float(x['close']) for x in k_lines[-6:-1]]
    mad_5_pre = np.mean(close_5_pre).round(2)
    print("上一个5日均线%s" % mad_5_pre)

    mad_5_angle = round(math.atan((mad_5 / mad_5_pre - 1) * 100) * 180 / 3.1415926, 2)
    print('角度%s', mad_5_angle)

    close_20 = [float(x['close']) for x in k_lines[-20:]]
    s = sum(close_20)
    mad_20 = np.mean(close_20).round(2)
    print("20日均线%s" % mad_20)

    close_20_pre = [float(x['close']) for x in k_lines[-21:-1]]

    mad_20_pre = np.mean(close_20_pre).round(2)
    print("上一个20日均线%s" % mad_20_pre)

    mad_20_angle = round(math.atan((mad_20 / mad_20_pre - 1) * 100) * 180 / 3.1415926, 2)
    print('20日角度%s', mad_20_angle)
    return {'mad_5': mad_5, 'mad_5_angle': mad_5_angle, 'mad_20': mad_20, 'mad_20_angle': mad_5_angle}


if __name__ == '__main__':
    # main_1()
    k_minute = 5
    stock_code = '600029'
    build = EastmoneyRequestbuild()
    trend2_json = build.get_stock_trends2(stock_code)
    stock_k_line_history = build.get_stock_kline(k_minute, stock_code)

    if trend2_json is None:
        raise Exception('数据加载失败')

    trends_array = trend2_json['data']['trends']
    trends = []
    for trend_str in trends_array:
        # time0 open1 close2 min3 max4 vol5 tag6 macd7 dif8 dea9
        # '2021-05-28 09:30,6.79,6.79,6.79,6.79,2425,1646575.00,6.790'
        time_str, open, close, min, max, volume, amount, averages = trend_str.split(',')
        data = {'time': time_str, 'open': open, 'close': close, "volume": volume, "amount": amount,
                "averages": averages}
        trends.append(data)
        k_line_array = stock_k_line_history['data']['klines']
    lines_data = []
    for k_line in k_line_array:
        time_str, open, close, high, low, volume, amount, _, _, _, _ = k_line.split(',')
        now_date_format = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                            datetime.datetime.now().day,
                                            0, 0).strftime('%Y-%m-%d')
        if now_date_format in time_str:
            continue
        lines_data.append({"time_str": time_str, "close": close})
    result_dict = get_current_real_time(trends, lines_data, k_minute)
