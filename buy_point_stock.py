import datetime

from bao_stock_api import SqlAction
from my_email import MailUtils
from option import Result, Option, Ok, Err

'''
http://vrg123.com/ pycharm激活
option 文档
https://mat1g3r.github.io/option/
'''


def buy_point_1(now_date, content):
    results = SqlAction.get_buy_point_stock_info()

    if len(results) > 0:
        line_tables = ''
        updated_array = []
        for (code_name, code, date, close, mad_5, mad_10, mad_20, mad_5_angle, mad_10_angle, mad_20_angle) in results:
            updated_array.append(code)
            line_table = '''
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            ''' % (code_name, code, close, mad_5, mad_10, mad_20)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐一' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_buy_point_stock_info(updated_array)
            return Ok("股票推荐一发送成功!")
        return Err(None)
    return Err(None)


def buy_point_2(now_date, content) :
    results2 = SqlAction.get_all_buy_point_stock_info()
    if len(results2) > 0:
        line_tables = ''
        updated_array = []
        for (code_name, code, date, close, mad_5, mad_10, mad_20, mad_5_angle, mad_10_angle, mad_20_angle) in results2:
            updated_array.append(code)
            line_table = '''
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
                    ''' % (code_name, code, close, mad_5, mad_10, mad_20)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐二' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_all_buy_point_stock_info(updated_array)
            return Ok("股票推荐一发送成功!")
        return Err(None)
    return Err(None)
def buy_point_3(now_date ,content):
    results2 = SqlAction.get_low_point_up_stock_info()
    if len(results2) > 0:
        line_tables = ''
        updated_array = []
        for (code_name, code, date, close, low_4_percent, low_8_percent, low_10_percent) in results2:
            updated_array.append(code)
            line_table = '''
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
                    ''' % (code_name, code, close, low_4_percent, low_8_percent, low_10_percent)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐--近20日最低价' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_low_point_up_stock_info(updated_array)
            return Ok("股票推荐--近20日最低价发送成功!")
        return Err(None)
    return Err(None)


def buy_point_4(now_date, content):
    results2 = SqlAction.get_turn_rate_stock_info()
    if len(results2) > 0:
        line_tables = ''
        updated_array = []
        for (code_name, code, date, close, turn) in results2:
            updated_array.append(code)
            line_table = '''
                       <tr>
                           <td>%s  </td>
                           <td>%s</td>
                           <td>%s</td>
                           <td>%s</td>
                       </tr>
                       ''' % (code_name, code, close, turn)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐--连续2日上涨,成交量翻倍,均线斜率大于30度' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_turn_rate_stock_info(updated_array)
            return Ok("股票推荐----连续2日上涨,成交量翻倍,均线斜率大于30度发送成功!")
        return Err(None)
    return Err(None)


if __name__ == '__main__':
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    content = '''
    <!-- CSS goes in the document HEAD or added to your external stylesheet -->
<style type="text/css">
table.gridtable {
    font-family: verdana,arial,sans-serif;
    font-size:11px;
    color:#333333;
    border-width: 1px;
    border-color: #666666;
    border-collapse: collapse;
}
table.gridtable th {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #dedede;
}
table.gridtable td {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #ffffff;
}
</style>
 
<!-- Table goes in the document BODY -->
<table class="gridtable">
<tr>
    <th>股票名称</th>
    <th>股票代码</th>
    <th>收盘价</th>
    <th>5mad</th>
    <th>10mad</th>
    <th>20mad</th>
</tr>
%s
</table>

    
    '''
    #result = buy_point_1(now_date, content)
    # if result.is_ok:
    #     print(result.unwrap())
    #result2 = buy_point_2(now_date, content)
    #if result2.is_ok:
        #print(result2.unwrap())
    # result2 = buy_point_3(now_date, content)
    # if result2.is_ok:
    #     print(result2.unwrap())

    result4 = buy_point_4(now_date, content)
    if result4.is_ok:
        print(result4.unwrap())
