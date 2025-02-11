import time

import pymysql
from config.config import conf

from playwright.sync_api import Playwright, sync_playwright, expect

keywords = ['金融', '市场', '财经', '股市', 'a股', '大a', '宝妈', '程序员', '大数据', '分析', '理财', '投资', '产业', '基金',
            '创业', '职场', 'it', '大厂', '期货', '读书', '个人成长', '规划', '职业', '教育', '技能', '婚姻', '开发', '编程',
            '币圈', '美股', '虚拟', '技术', '银行', '环球', 'ai', '地产', '能源', '保险', '互联网', 'web3', '货币', '余额宝',
            '固收', '物联网', '元宇宙', '中东', '华为', '苹果', '数码', '摄影', '芯片', '光刻机', '封测', '消费', '电子', '运维',
            '房贷', '服务器', '机器人', '智能', '股指', '期权', '阿里', '腾讯', '律所', '四大', 'gpt', '启发', '算法', '985',
            'QS']
# keywords = ['机器人', '启发']
first = 1
last = -1
site = 'https://public.zsxq.com'
run_flag = True
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']

def run(pw: Playwright, keyword: str) -> None:
    try:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )

        page = context.new_page()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db, charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        global first
        while True:
            url = 'https://www.bing.com/search?q=' + keyword + '+site:' + site + '&first=' + str(first) + '&FORM=PORE'
            print(url)
            page.goto(url)
            time.sleep(5)
            list = page.locator("ol#b_results>li.b_algo>h2>a").all()
            id_list = []
            for item in list:
                url = item.get_attribute('href')
                if url.startswith('https://public.zsxq.com/groups/'):
                    last_id = url.replace('https://public.zsxq.com/groups/', '')
                    digit_id = ''
                    for id_key in last_id:
                        if id_key.isdecimal():
                            digit_id = digit_id + id_key
                        else:
                            break
                    id_list.append(digit_id)
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
            for key in keywords:
                print(key)
                run(playwright, key)
                first = 1
            break
        except Exception as e:
            print(e)
