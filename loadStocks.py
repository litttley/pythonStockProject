from bao_stock_api import BaoStockApi, SqlAction

if __name__ == '__main__':
    # 登陆系统
    bsApi = BaoStockApi()
    if bsApi.isLogin:
        # 获取上证50成分股
        sz50_stocks, sz50_fields = bsApi.query_sz50_stocks()
        # 沪深300成分股
        hs300_stocks, hs300_fields = bsApi.query_hs300_stocks()
        # 中证500成分股
        sz500_stocks, sz500_fields = bsApi.query_zz500_stocks()
        # print(sz50_stocks)
        # print(fields)
        SqlAction.insert_codes(sz50_stocks)
        SqlAction.insert_codes(hs300_stocks)
        SqlAction.insert_codes(sz500_stocks)
