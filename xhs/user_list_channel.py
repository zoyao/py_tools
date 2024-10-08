import time

import pymysql
from config.config import conf

from playwright.sync_api import Playwright, sync_playwright, expect

channels = ['homefeed_recommend', 'binggaokao_feed_recommend', 'homefeed.career_v3', 'homefeed.love_v3',
            'homefeed.household_product_v3', 'homefeed.travel_v3']
page_max = 100
url = 'https://www.xiaohongshu.com/explore?channel_id='
run_flag = True
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

def run(pw: Playwright) -> None:
    try:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )
        page = context.new_page()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        for channel in channels:
            print(url + channel)
            page.goto(url + channel)
            for i in range(10):
                login_close_button = page.locator("div.icon-btn-wrapper.button.close").all()
                if len(login_close_button) > 0:
                    login_close_button[0].click()
                    break
                time.sleep(1)
            for i in range(page_max):
                # 光标移动至滚动条所在框中
                page.click("#global > div.main-container")
                # 滚动鼠标 , 参数给一个较大值，以保证直接移动至最后
                page.mouse.wheel(0, 10000)
                time.sleep(1)
            user_list = page.locator("div.footer>div.author-wrapper>a").all()
            for user in user_list:
                user_href = user.get_attribute('href')
                user_id = user_href.replace('/user/profile/', '').split('?')[0]
                insert_query = """
                                    INSERT IGNORE INTO bs_user_xhs
                                    (id)
                                    VALUES (%s)
                               """
                cursor.execute(insert_query, user_id)
                conn.commit()
            time.sleep(5)

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
    try:
        run(playwright)
    except Exception as e:
        print(e)
