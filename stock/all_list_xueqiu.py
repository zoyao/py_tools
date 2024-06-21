import requests
import pymysql
from config.config import conf

max_insert_num = 100
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

index = 0
max_size = 100
while True:
    index += 1
    response = requests.get('https://stock.xueqiu.com/v5/stock/screener/quote/list.json?' +
                            'page=' + str(index) + '&size=' + str(max_size) +
                            '&order=desc&order_by=percent&market=CN&type=sh_sz')
    if response.status_code == 200:
        json = response.json()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        for i in range(0, len(json), max_insert_num):
            list = json[i:i + max_insert_num]
            insert_query = """
                            INSERT INTO bs_stock
                            (stock_code, stock_name, stock_type, update_time)
                            """
            for j in list:
                insert_query += """
                                VALUES (%s, %s, 0, CURRENT_TIMESTAMP)
                                """
            insert_query += """
                            ON DUPLICATE KEY UPDATE
                            stock_name = VALUES(stock_name),
                            stock_type = VALUES(stock_type)
                            """
            values = ()
            for stock in list:
                values.__add__(stock['symbol'])
                values.__add__(stock['name'])
            print(values)
            cursor.execute(insert_query, values)
            conn.commit()
        if index * max_size >= json['data']['count']:
            break
