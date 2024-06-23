import requests
import pymysql
from config.config import conf

config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

response = requests.get("http://api.mairui.club/hslt/list/" + licence)
if response.status_code == 200:
    json = response.json()
    conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    for stock in json:
        insert_query = """
                        INSERT INTO bs_stock
                        (stock_code, stock_name, stock_type, update_time)
                        VALUES (%s, %s, 0, CURRENT_TIMESTAMP)
                        ON DUPLICATE KEY UPDATE
                        stock_name = VALUES(stock_name)
                        """
        values = (stock['jys'] + stock['dm'], stock['mc'])
        print(values)
        cursor.execute(insert_query, values)
        conn.commit()
