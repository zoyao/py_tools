import pymysql
from config.config import conf
from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


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
test = 1

while True:
    index += 1
    url = 'https://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?indexid=000300&page=' + str(index)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到包含class为'e1'的元素
    elements = soup.findAll('table', id='NewStockTable')[0].findAll('tr')
    conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db,
                           charset='utf8mb4')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if elements is not None and len(elements) > 0:
        flag = False
        values = ()
        insert_query = """
                        INSERT INTO bs_stock_hs300
                        (stock_code, stock_name, update_time)
                        VALUES
                            """
        for element in elements:
            a = element.findAll('a')
            if a is not None and len(a) > 0:
                name = a[0].text
                code = a[0].attrs.get('href').replace('http://finance.sina.com.cn/realstock/company/', '').replace('/nc.shtml', '')
                print(code + '\t' + name)
                test += 1
                if flag:
                    insert_query += """
                                    ,
                                    """
                flag = True
                insert_query += """
                             (%s, %s, CURRENT_TIMESTAMP)
                                """
                values = values + (code, name)

        insert_query += """
                                        ON DUPLICATE KEY UPDATE
                                        stock_name = VALUES(stock_name)
                                        """
        # print(values)
        cursor.execute(insert_query, values)
        conn.commit()
