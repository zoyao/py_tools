import pymysql
from config.config import conf
import asyncio

from playwright.async_api import Playwright, async_playwright

max_threads = 10
max_pages = 10
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
            code = result['stock_code']
            url = 'https://xueqiu.com/S/' + code
            await page.goto(url)

            # 关闭两个弹窗
            closes = await page.locator(
                '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div > div > a').all()
            for close in closes:
                await close.click()
            closes = await page.locator(
                '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login.modal__login__jianlian > div > div > a').all()
            for close in closes:
                await close.click()
            values = ()
            for i in range(max_pages):
                null_num = await page.locator('#app > div.container > div.container-404 > div.container-404__bg').count()
                if null_num > 0:
                    break
                try:
                    await page.wait_for_selector('//*[@class="timeline__item__info"]/div/a[1]')
                except Exception as e:
                    break
                list = await page.locator('//*[@class="timeline__item__info"]/div/a[1]').all()
                for item in list:
                    user_name = await item.inner_html()
                    user_url = await item.get_attribute('href')
                    user_id = await item.get_attribute('data-tooltip')
                    if not user_id.isdigit():
                        continue
                    values = values + (user_id, user_name, user_url)
                next_num = await page.locator('a.pagination__next[style*="display: none;"]').count()
                if next_num > 0:
                    break
                else:
                    await page.locator('a.pagination__next').click()

            if len(values) > 0:
                insert_query = """
                        INSERT INTO bs_xueqiu_user
                        (user_id, user_name, user_url)
                        VALUES 
                                """
                flag = False
                for i in range(int(len(values) / 3)):
                    if flag:
                        insert_query += """
                                        ,
                                        """
                    flag = True
                    insert_query += """
                        (%s, %s, %s)
                    """
                insert_query += """
                        ON DUPLICATE KEY UPDATE 
                        user_id = VALUES(user_id)          
                    """
                print(values)
                cursor.execute(insert_query, values)
                conn.commit()

            insert_query = """
                    update bs_stock
                    set status_xueqiu = 2
                    where stock_type = %s
                    and stock_code = %s    
                """
            values = (result['stock_type'], result['stock_code'])
            cursor.execute(insert_query, values)
            conn.commit()
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
            select stock_type, stock_code from bs_stock where status_xueqiu = 1
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
