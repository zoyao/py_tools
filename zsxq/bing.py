import random
import time

import pymysql


from playwright.sync_api import Playwright, sync_playwright, expect


keyword = '市场'
first = 1
last = -1
site = 'https://public.zsxq.com'
run_flag = True

def run(pw: Playwright) -> None:
    try:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )

        page = context.new_page()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        global first
        while True:
            url = 'https://www.bing.com/search?q=' + keyword + '+site:' + site + '&first=' + str(first) + '&FORM=PORE'
            print(url)
            page.goto(url)
            list = page.locator("#b_results>.b_algo>h2>a").all()
            id_list = []
            for item in list:
                url = item.get_attribute('href')
                if url.startswith('https://public.zsxq.com/groups/'):
                    last_id = (url.replace('https://public.zsxq.com/groups/', '')
                               .replace('.html', '').replace('?s=bd&v=1', ''))
                    last_id = last_id.split('?')[0]
                    id_list.append(last_id)
                else:
                    id_list.append(None)
            if len(id_list) <= 0 or 0 < last <= first:
                global run_flag
                run_flag = False
                break
            for last_id in id_list:
                first += 1
                if not last_id:
                    continue
                try:
                    url = 'https://public.zsxq.com/groups/' + last_id + '.html'
                    page.goto(url)
                    divs = page.locator("main>div").all()
                    if len(divs) > 3:
                        name = page.locator("main>.preview>.right>.top>h3").first.inner_html()
                        member_info_list = page.locator("main>.preview>.right>.top>div>span").all()
                        update_time = member_info_list[1].inner_html()
                        member_info = member_info_list[0].inner_html() + update_time
                        member_count = None
                        if len(member_info_list) > 2:
                            member_count = member_info_list[3].inner_html().replace(' ', '').replace('\n', '')
                            member_info = member_info_list[0].inner_html() + update_time + \
                                      member_info_list[2].inner_html().replace('&nbsp;', '') + member_count
                        topic_info_list = page.locator("main>.preview>.right>.topic-info>span").all()
                        run_day = topic_info_list[1].inner_html()
                        topic_info = topic_info_list[0].inner_html() + run_day + \
                                     topic_info_list[2].inner_html().replace(' ', '').replace('\n', '')
                        update_content = topic_info_list[2].inner_html().replace(' ', '').replace('\n', '') \
                            .replace('天，更新了', '').replace('篇内容', '')
                        price_locator = page.locator("main>.join>.price-container>.price")
                        price = ''
                        if price_locator.count() > 0:
                            price = price_locator.first.inner_html()
                        desc = (page.locator("main>.group-info>.desc").first.inner_html().
                                replace(' ', '').replace('\n',''))

                        price_num = 0
                        if price.startswith('￥'):
                            try:
                                price_num = int(price.replace('￥', ''))
                            except Exception as e:
                                print(e)

                        member_num = 0
                        if member_count:
                            try:
                                member_num = int(member_count.replace('+', ''))
                            except Exception as e:
                                print(e)

                        update_time_num = -1
                        if update_time:
                            try:
                                if update_time == '刚刚':
                                    update_time_num = 0
                                elif update_time.endswith('小时前'):
                                    update_time_num = int(update_time.replace('小时前', ''))
                                elif update_time.endswith('天前'):
                                    update_time_num = int(update_time.replace('天前', '')) * 24
                            except Exception as e:
                                    print(e)

                        insert_query = """
                            INSERT INTO dy_zsxq_result
                            (id, group_name, url, update_time, member_count, member_info, run_day, update_content, 
                            topic_info, price, group_desc, price_num, member_num, update_time_num, sys_time)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                            ON DUPLICATE KEY UPDATE 
                            group_name = VALUES(group_name),
                            url = VALUES(url),
                            update_time = VALUES(update_time),
                            member_count = VALUES(member_count),
                            member_info = VALUES(member_info),
                            run_day = VALUES(run_day),
                            update_content = VALUES(update_content),
                            topic_info = VALUES(topic_info),
                            price = VALUES(price),
                            group_desc = VALUES(group_desc),
                            price_num = VALUES(price_num),
                            member_num = VALUES(member_num),
                            update_time_num = VALUES(update_time_num),
                            sys_time = VALUES(sys_time)
                        """
                        values = (last_id, name, url, update_time, member_count, member_info, run_day, update_content,
                                  topic_info, price, desc, price_num, member_num, update_time_num)

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
    while run_flag:
        try:
            run(playwright)
            break
        except Exception as e:
            print(e)
