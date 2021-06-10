import datetime

from eastmoneyapi.east_money_api import EastmoneyRequestbuild

if __name__ == '__main__':
    k_minute = EastmoneyRequestbuild.minute_k_type.get('minute_k_30')
    stock_code = 'sz.000156'
    build = EastmoneyRequestbuild()
    trend2_json = build.get_stock_trends2(stock_code.replace('sh', '1').replace('sz', '0'))
    stock_k_line_history = build.get_stock_kline(k_minute, stock_code.replace('sh', '1').replace('sz', '0'))

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
    result_dict = build.get_current_real_time(trends, lines_data, k_minute)
