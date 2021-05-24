import pymysql
from dbutils.pooled_db import PooledDB


class MySqlPool(object):
    config = {
        'creator': pymysql,
        'host': "localhost",
        'port': 3306,
        'user': "root",
        'password': "root",
        'db': "bao_stock_data",
        'charset': 'utf8',
        'maxconnections': 70,  # 连接池最大连接数量
        'cursorclass': pymysql.cursors.DictCursor
    }
    pool = PooledDB(**config)

    def __init__(self):
        self.conn = MySqlPool.pool.connection()

    # 执行withjf的代码块后自动调用该函数
    def __enter__(self):
        self.conn = MySqlPool.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    # 执行完with后面的代码块后自动调用该函数
    def __exit__(self, type, value, trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


