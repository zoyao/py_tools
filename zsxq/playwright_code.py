import pymysql
from config.config import conf

from playwright.sync_api import Playwright, sync_playwright, expect

config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

def run(pw: Playwright) -> None:
    try:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )

        page = context.new_page()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        while True:
            cursor.execute("INSERT INTO dy_zsxq_check () VALUES ()")
            last_id = str(cursor.lastrowid)
            conn.commit()

            url = 'https://public.zsxq.com/groups/' + last_id + '.html'
            page.goto(url)
            divs = page.locator("main>div").all()
            if len(divs) > 3:
                name = page.locator("main>.preview>.right>.top>h3").first.inner_html()
                member_info_list = page.locator("main>.preview>.right>.top>div>span").all()
                update_time = member_info_list[1].inner_html()
                member_count = member_info_list[3].inner_html().replace(' ', '').replace('\n', '')
                member_info = member_info_list[0].inner_html() + update_time + \
                              member_info_list[2].inner_html().replace('&nbsp;', '') + member_count
                topic_info_list = page.locator("main>.preview>.right>.topic-info>span").all()
                run_day = topic_info_list[1].inner_html()
                topic_info = topic_info_list[0].inner_html() + run_day + \
                             topic_info_list[2].inner_html().replace(' ', '').replace('\n', '')
                update_content = topic_info_list[2].inner_html().replace(' ', '').replace('\n', '')\
                    .replace('天，更新了', '').replace('篇内容', '')
                price = page.locator("main>.join>.price-container>.price").first.inner_html()
                desc = page.locator("main>.group-info>.desc").first.inner_html().replace(' ', '').replace('\n', '')

                insert_query = """
                            INSERT INTO dy_zsxq_result 
                            (id, group_name, url, update_time, member_count, member_info, 
                            run_day, update_content, topic_info, price, group_desc)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                values = (last_id, name, url, update_time, member_count, member_info,
                          run_day, update_content, topic_info, price, desc)
                cursor.execute(insert_query, values)
                conn.commit()
            cursor.execute("delete from dy_zsxq_check where id = " + last_id)
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn:
            try:
                conn.commit()
            except Exception as e:
                print(e)
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    print(e)
                if conn:
                    try:
                        conn.close()
                    except Exception as e:
                        print(e)
        if page:
            try:
                page.close()
            except Exception as e:
                print(e)
        if context:
            try:
                context.close()
            except Exception as e:
                print(e)
        if browser:
            browser.close()


with sync_playwright() as playwright:
    while True:
        try:
            run(playwright)
        except Exception as e:
            print(e)
