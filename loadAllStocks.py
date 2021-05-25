from bao_stock_api import BaoStockApi, SqlAction

if __name__ == '__main__':
    # 登陆系统
    bsApi = BaoStockApi()
    if bsApi.isLogin:
        # 获取上证50成分股
        all_stocks, sz50_fields = bsApi.query_stock_basic()
        SqlAction.insert_all_codes(all_stocks)



