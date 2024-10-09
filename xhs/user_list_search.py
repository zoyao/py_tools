import time

import pymysql
from config.config import conf

from playwright.sync_api import Playwright, sync_playwright, expect

keywords = ['股票', '基金', '私募']
page_max = 50
url = 'https://www.xiaohongshu.com/search_result?source=web_explore_feed&keyword='
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
        for keyword in keywords:
            print(url + keyword)
            page.goto(url + keyword)
            for i in range(10):
                login_close_button = page.locator("div.icon-btn-wrapper.button.close").all()
                if len(login_close_button) > 0:
                    break
                time.sleep(1)
            tabs = page.locator("#global > div.main-container > div.with-side-bar.main-content > div > "
                                "div.reds-sticky-box > div > div > div.content-container > button.tab").all()
            for tab in tabs:
                tab.click()
                user_list = set()
                list_new = page.locator("div.footer>div.author-wrapper>a").all()
                if len(list_new) > 0:
                    for new in list_new:
                        user_href = new.get_attribute('href')
                        user_id = user_href.replace('/user/profile/', '').split('?')[0]
                        user_list.add(user_id)
                size = len(user_list)
                error_num = 0
                for i in range(page_max):
                    # 光标移动至滚动条所在框中
                    page.click("#global > div.main-container")
                    # 滚动鼠标 , 参数给一个较大值，以保证直接移动至最后
                    page.mouse.wheel(0, 10000)
                    time.sleep(1)
                    list_new = page.locator("div.footer>div.author-wrapper>a").all()
                    if len(list_new) > 0:
                        for new in list_new:
                            user_href = new.get_attribute('href')
                            user_id = user_href.replace('/user/profile/', '').split('?')[0]
                            user_list.add(user_id)
                    if len(user_list) <= size:
                        error_num += 1
                        if error_num > 5:
                            break
                    else:
                        error_num = 0
                        size = len(user_list)
                for user_id in user_list:
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
