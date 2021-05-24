import baostock as bs
import pandas as pd
from dbPools import MySqlPool


class BaoStockApi(object):

    def __init__(self):
        login = bs.login()
        if login.error_msg == "success":
            print("登录成功")
            print('login respond error_code:' + login.error_code)
            print('login respond  error_msg:' + login.error_msg)
            self.isLogin = True
        else:
            print("登录错误")
            print('login respond error_code:' + login.error_code)
            print('login respond  error_msg:' + login.error_msg)
            self.isLogin = False

    def query_sz50_stocks(self):
        rs = bs.query_sz50_stocks()
        print('query_sz50 error_code:' + rs.error_code)
        print('query_sz50  error_msg:' + rs.error_msg)
        # 打印结果集
        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            sz50_stocks.append(rs.get_row_data())
        return sz50_stocks, rs.fields

    def query_hs300_stocks(self):

        rs = bs.query_hs300_stocks()
        print('query_hs300 error_code:' + rs.error_code)
        print('query_hs300  error_msg:' + rs.error_msg)
        # 打印结果集
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            hs300_stocks.append(rs.get_row_data())
        return hs300_stocks, rs.fields

    def query_zz500_stocks(self):

        rs = bs.query_zz500_stocks()
        print('query_zz500 error_code:' + rs.error_code)
        print('query_zz500  error_msg:' + rs.error_msg)
        # 打印结果集
        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            zz500_stocks.append(rs.get_row_data())
        return zz500_stocks, rs.fields

    def query_history_k_data_plus(self, stock_code, start_date, end_date):
        # 获取沪深A股历史K线数据
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus(stock_code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,"
                                          "tradestatus,pctChg,isST",
                                          start_date=start_date, end_date=end_date,
                                          frequency="d", adjustflag="3")
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
        # 打印结果集
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        return data_list, rs.fields
    def query_all_stock(self):
        rs = bs.query_all_stock()
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        return data_list, rs.fields

def db_conn(func):
    def wrapper(*args, **kw):
        with MySqlPool() as db:
            result = func(db, *args, **kw)
        return result

    return wrapper


class SqlAction(object):
    def __init__(self):
        # self.conn = MySqlPool().conn
        pass

    @staticmethod
    @db_conn
    def insert_codes(db, stocks):
        sql = "SELECT code FROM codes"
        insert_sql = 'INSERT INTO codes (updateDate ,code,  code_name) VALUES (%s, %s, %s)'
        insert_sql_arr = []
        update_sql = 'UPDATE `codes` SET `updateDate` = %s, `code_name` = %s WHERE `code` = %s;'
        update_sql_arr = []

        try:

            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            if not results:  # 结果为空

                for (date, code, code_name) in stocks:
                    insert_sql_arr.append((date, code, code_name))

            else:
                code_set = set(result['code'] for result in results)

                for (date, code, code_name) in stocks:
                    if code in code_set:  # 已存在数据库中更新
                        update_sql_arr.append((date, code_name, code))
                    else:
                        insert_sql_arr.append((date, code, code_name))
            if len(insert_sql_arr) != 0:
                excute_result = db.cursor.executemany(insert_sql, insert_sql_arr)
                print('执行插入成功%s条数据' % excute_result)
            if len(update_sql_arr) != 0:
                excute_result = db.cursor.executemany(update_sql, update_sql_arr)
                print('执行更新成功%s条数据' % excute_result)
            return True

        except Exception as  e:
            print(e)
            return False

    @staticmethod
    @db_conn
    def get_day_data_code_list(db):
        sql = 'SELECT  distinct code FROM day_data'
        try:
            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            result = [x['code'] for x in results]
            return result
        except Exception as e:
            print(e)
            return []

    @staticmethod
    @db_conn
    def get_codes_code_list(db):
        sql = 'SELECT  distinct code FROM codes'
        try:
            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            result = [x['code'] for x in results]
            return result
        except Exception as e:
            print(e)
            return []

    @staticmethod
    @db_conn
    def insert_day_date(db, day_data, mad_5, mad_10, mad_20,mad_5_angle,mad_10_angle,mad_20_angle):

        try:
            insert_sql = 'INSERT INTO `day_data` (`code`, `date`, `open`, `high`, `low`, `close`, `preclose`, `volume`, `amount`, `adjustflag`, `turn`, `tradestatus`, `ctChg`,  `isST`,`mad_5`,`mad_10`,`mad_20`,`mad_5_angle`,`mad_10_angle`,`mad_20_angle`)' \
                         ' VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s,  %s,%s,%s,%s,%s,%s,%s);'
            insert_array = []
            date, code, open, high, low, close, preclose, volume, amount, adjustflag, turn, tradestatus, pctChg, isST = \
            day_data[0]

            insert_array.append(
                (code, date, open, high, low, close, preclose, volume, amount, adjustflag, turn, tradestatus, pctChg,
                 isST, mad_5, mad_10, mad_20,mad_5_angle,mad_10_angle,mad_20_angle))
            excute_result = db.cursor.executemany(insert_sql, insert_array)
            print(excute_result)
            print('执行插入成功%s条数据' % excute_result)
        except Exception as e:
            print(e)
            print(insert_array)


if __name__ == '__main__':
    # 登陆系统
    bsApi = BaoStockApi()
    if bsApi.isLogin:
        # 获取上证50成分股
        sz50_stocks, fields = bsApi.query_sz50_stocks()
        print(sz50_stocks)
        print(fields)
        SqlAction.insert_codes(sz50_stocks)

        # result = pd.DataFrame(sz50_stocks, columns=fields)
        # 结果集输出到csv文件
        # result.to_csv("D:/sz50_stocks.csv", encoding="gbk", index=False)

    # print(result)
