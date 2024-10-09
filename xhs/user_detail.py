import time

import pymysql
from config.config import conf

from playwright.sync_api import Playwright, sync_playwright, expect

url = 'https://www.xiaohongshu.com/user/profile/'
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']


def get_span_count(span_count: str):
    span_count = span_count.replace('+', '').replace(' ', '')
    if span_count.find('亿') >= 0:
        span_count = span_count.replace('亿', '')
        return int(span_count) * 100000000
    if span_count.find('千万') >= 0:
        span_count = span_count.replace('千万', '')
        return int(span_count) * 10000000
    if span_count.find('百万') >= 0:
        span_count = span_count.replace('百万', '')
        return int(span_count) * 1000000
    if span_count.find('十万') >= 0:
        span_count = span_count.replace('十万', '')
        return int(span_count) * 100000
    if span_count.find('万') >= 0:
        span_count = span_count.replace('万', '')
        return int(span_count) * 10000
    if span_count.find('千') >= 0:
        span_count = span_count.replace('千', '')
        return int(span_count) * 1000
    return int(span_count)


def run(pw: Playwright) -> None:
    try:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )
        page = context.new_page()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        select_query = """
            select id from bs_user_xhs where update_time is null
        """
        cursor.execute(select_query)
        results = cursor.fetchall()
        for item in results:
            user_id = item['id']
            print(url + user_id)
            try:
                page.goto(url + user_id)

                user_name = None
                user_code = None
                user_ip = None
                user_tag = None
                follow_count = 0
                fans_count = 0
                like_count = 0

                user_name_all = page.locator('#userPageContainer > div.user > div > div.info-part > div.info > '
                                             'div.basic-info > div.user-basic > div.user-nickname > div').all()
                if len(user_name_all) > 0:
                    user_name = user_name_all[0].text_content()
                user_code_all = page.locator('#userPageContainer > div.user > div > div.info-part '
                                             '> div.info > div.basic-info > div.user-basic > div.user-content > '
                                             'span.user-redId').all()
                if len(user_code_all) > 0:
                    user_code = user_code_all[0].text_content().replace('小红书号：', '')
                user_ip_all = page.locator('#userPageContainer > div.user > div > div.info-part > div.info > '
                                           'div.basic-info > div.user-basic > div.user-content > span.user-IP').all()
                if len(user_ip_all) > 0:
                    user_ip = user_ip_all[0].text_content().replace(' IP属地：', '')
                user_tag_all = page.locator('#userPageContainer > div.user > div > div.info-part > div.info > '
                                            'div.user-tags > div').all()
                if len(user_tag_all) > 0:
                    user_tag = ''
                    for tag in user_tag_all:
                        user_tag += tag.text_content()
                count_all = page.locator('#userPageContainer > div.user > div > div.info-part > div.info > div.data-info > '
                                         'div > div').all()
                if len(count_all) > 0:
                    for count_item in count_all:
                        span_count_all = count_item.locator('span.count').all()
                        span_show_all = count_item.locator('span.shows').all()
                        if len(span_show_all) > 0 and len(span_count_all) > 0:
                            span_show = span_show_all[0].text_content()
                            span_count = span_count_all[0].text_content()
                            if '关注' == span_show:
                                follow_count = get_span_count(span_count)
                            elif '粉丝' == span_show:
                                fans_count = get_span_count(span_count)
                            elif '获赞与收藏' == span_show:
                                like_count = get_span_count(span_count)
                pass
                insert_query = """
                                    update bs_user_xhs
                                    set code = %s,
                                    name = %s,
                                    ip_address = %s,
                                    tags = %s,
                                    follow_num = %s,
                                    fans_num = %s,
                                    like_num = %s,
                                    update_time = CURRENT_TIMESTAMP
                                    where id = %s
                                """
                values = (user_code, user_name, user_ip, user_tag, follow_count, fans_count, like_count, user_id)
                cursor.execute(insert_query, values)
                conn.commit()
            except Exception as e:
                print(e)
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
