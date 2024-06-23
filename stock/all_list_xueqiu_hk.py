import pymysql
from config.config import conf
from requests_html import HTMLSession


max_insert_num = 100
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

max_size = 90

index = 0
session = HTMLSession()
session.get('https://xueqiu.com/hq/detail?market=CN&first_name=0&second_name=0&type=sh_sz')

while True:
    index += 1
    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=' + str(index) + '&size=' + \
            str(max_size) + '&order=desc&order_by=percent&market=HK&type=hk&is_delay=true'
    response = session.get(url)
    conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db,
                           charset='utf8mb4')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if response.status_code == 200:
        json = response.json()
        if json is None or json == {} or json['data'] is None or json['data'] == {} or \
                json['data']['list'] is None or json['data']['list'] == {} or json['data']['list'] == []:
            break
        for i in range(0, len(json['data']['list']), max_insert_num):
            list = json['data']['list'][i:i + max_insert_num]
            insert_query = """
                            INSERT INTO bs_stock
                            (stock_code, stock_name, stock_type, update_time)
                            VALUES
                                """
            flag = False
            for j in list:
                if flag:
                    insert_query += """
                                    ,
                                    """
                flag = True
                insert_query += """
                             (%s, %s, 1, CURRENT_TIMESTAMP)
                                """
            insert_query += """
                            ON DUPLICATE KEY UPDATE
                            stock_name = VALUES(stock_name)
                            """
            values = ()
            for stock in list:
                values = values + (stock['symbol'], stock['name'])
            print(values)
            cursor.execute(insert_query, values)
            conn.commit()


