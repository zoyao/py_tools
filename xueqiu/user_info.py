import pymysql
from config.config import conf
import asyncio

from playwright.async_api import Playwright, async_playwright

max_threads = 10
config = conf().get_config()
licence = config['mairui']['licence']
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']
mysql_user = config['mysql']['user']
mysql_password = config['mysql']['password']
mysql_db = config['mysql']['db']
results = []
error = 0


async def run(pw: Playwright) -> bool:
    global error
    try:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )
        page = await context.new_page()
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db,
                               charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        while True:
            try:
                result = results.pop(0)
            except IndexError as e:
                return False
            code = result['user_url']
            url = 'https://xueqiu.com' + code
            await page.goto(url)

            # 关闭两个弹窗
            # closes = await page.locator(
            #     '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div > div > a').all()
            # for close in closes:
            #     await close.click()
            # closes = await page.locator(
            #     '#app > div.modals.dimmer.js-shown > div:nth-child(1) > '
            #     'div.modal.modal__login.modal__login__jianlian > div > div > a').all()
            # for close in closes:
            #     await close.click()
            await page.locator('div.profiles__tabs > a.router-link-exact-active.active > span').all()

            count_follow = 0
            count_fans = 0
            count_post = 0
            count_column = 0
            column_name = None
            address = None
            address_ip = None
            introduction = None

            friendship_number = await page.locator('ul.friendship-number > li > a').count()
            if friendship_number > 0:
                friendships = await page.locator('ul.friendship-number > li > a').all()
                for friendship in friendships:
                    friendship_url = await friendship.get_attribute('href')
                    follows = await friendship.locator('strong').all()
                    if len(follows) > 0:
                        friendship_num = await follows[0].inner_html()
                        if friendship_num.isdigit():
                            if friendship_url.find('follow') >= 0:
                                count_follow = int(friendship_num)
                            elif friendship_url.find('fans') >= 0:
                                count_fans = int(friendship_num)
            address_number = await page.locator('ul.profiles__address > li').count()
            if address_number > 0:
                addresses = await page.locator('ul.profiles__address > li').all()
                for address_item in addresses:
                    address_a_number = await address_item.locator('a').count()
                    if address_a_number > 0:
                        continue
                    address_i_number = await address_item.locator('i.iconfont').count()
                    address_now = await address_item.inner_html()
                    if address_i_number > 0:
                        address = remove_str_html((address_now.replace('', '').replace('不限', '')
                                                   .replace('省/直辖市', '').replace('城市/地区', '')
                                                   .replace('\n', '').replace(' ', '')))
                    else:
                        address_ip = address_now.replace('IP属地：', '').replace(' ', '')

            info_number = await page.locator('div.profiles__hd__info > p').count()
            if info_number > 0:
                info = await page.locator('div.profiles__hd__info > p').all()
                introduction = await info[0].inner_html()

            post_number = await page.locator('div.profiles__tabs > a.router-link-exact-active.active > span').count()
            if post_number > 0:
                posts = await page.locator('div.profiles__tabs > a.router-link-exact-active.active > span').all()
                post_item = await posts[0].inner_html()
                if post_item.isdigit():
                    count_post = int(post_item)

            column_number = await page.locator('div.profiles__side > div.profiles__article__column > span').count()
            if column_number > 0:
                columns = await page.locator('div.profiles__side > div.profiles__article__column > span').all()
                column_item = await columns[0].inner_html()
                column_item = column_item.replace('篇文章', '')
                if column_item.isdigit():
                    count_column = int(column_item)

            column_name_number = await page.locator('div.profiles__side > div.profiles__article__column > h3 > a').count()
            if column_name_number > 0:
                column_names = await page.locator('div.profiles__side > div.profiles__article__column > h3 > a').all()
                column_name_item = await column_names[0].inner_html()
                column_name = remove_str_html(column_name_item)

            insert_query = """
                    update bs_xueqiu_user
                    set count_follow = %s,
                    count_fans = %s,
                    count_post = %s,
                    count_column = %s,
                    column_name = %s,
                    address = %s,
                    address_ip = %s,
                    introduction = %s,
                    update_time = CURRENT_TIMESTAMP
                    where user_id = %s
                """
            values = (count_follow, count_fans, count_post, count_column, column_name, address, address_ip,
                      introduction, result['user_id'])
            print(values)
            cursor.execute(insert_query, values)
            conn.commit()
            if count_follow > 0 or count_fans > 0 or count_post > 0 or count_column > 0 or column_name is not None or \
                    address is not None or address_ip is not None or introduction is not None:
                error = 0
    except Exception as e:
        print(e)
        error += 1
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(e)
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                print(e)
        try:
            if page:
                await page.close()
        except Exception as e:
            print(e)
        finally:
            try:
                if context:
                    await context.close()
            except Exception as e:
                print(e)
            finally:
                try:
                    if browser:
                        await browser.close()
                except Exception as e:
                    print(e)
    return True


def remove_str_html(word: str) -> str:
    while True:
        begin = word.find('<')
        end = word.find('>')
        if begin < 0 or end < 0 or end <= begin:
            break
        column_name_item_new = word[:begin] + word[end + 1:]
        word = column_name_item_new
    return word


async def start():
    async with async_playwright() as playwright:
        flag = True
        while flag:
            flag = await run(playwright)
            if error > 10:
                break


async def main():
    try:
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_password, db=mysql_db,
                               charset='utf8mb4')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        select_query = """
            select user_id, user_url from bs_xueqiu_user 
            where update_time is null
            or address_ip is null
        """
        cursor.execute(select_query)
        global results
        results = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()

    tasks = []
    for i in range(max_threads):
        tasks.append(start())
    await asyncio.gather(*tasks)

# 运行事件循环
asyncio.run(main())
