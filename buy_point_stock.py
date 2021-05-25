import datetime

from bao_stock_api import SqlAction
from my_email import MailUtils

if __name__ == '__main__':
    results = SqlAction.get_buy_point_stock_info()

    results2 = SqlAction.get_all_buy_point_stock_info()
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
    <th>时间</th>
    <th>股票代码</th>
    <th>收盘价</th>
    <th>5mad</th>
    <th>10mad</th>
    <th>20mad</th>
</tr>
%s
</table>

    
    '''

    if len(results) > 0:
        line_tables = ''
        updated_array = []
        for (code, date, close, mad_5, mad_10, mad_20, mad_5_angle, mad_10_angle, mad_20_angle) in results:
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
            ''' % (date, code, close, mad_5, mad_10, mad_20)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐1' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_buy_point_stock_info(updated_array)
    if len(results2) > 0:
        line_tables = ''
        updated_array = []
        for (code, date, close, mad_5, mad_10, mad_20, mad_5_angle, mad_10_angle, mad_20_angle) in results2:
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
                    ''' % (date, code, close, mad_5, mad_10, mad_20)
            line_tables = line_tables + line_table

        is_send = MailUtils().send_email('%s股票推荐2' % now_date, content % line_tables)
        if is_send:
            SqlAction.updated_all_buy_point_stock_info(updated_array)
