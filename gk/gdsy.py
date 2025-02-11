import time

from playwright.async_api import async_playwright, Playwright
import asyncio


async def run(pw: Playwright):
    # browser = pw.chromium.launch(headless=False)
    # browser = pw.chromium.launch_persistent_context(headless=False,
    #                                                 user_data_dir=r'C:\\Users\\zhong\\AppData\\Local\\Google\\Chrome\\User Data',
    #                                                 executable_path=r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    #                                                 args=["--start-maxmized",
    #                                                       # f"--disable-extensions-except={path_to_extension}",
    #                                                       # f"--load-extension={path_to_extension}",
    #                                                       '--disable-blink-features=AutomationControlled'],
    #                                                 accept_downloads=True,
    #                                                 bypass_csp=True,
    #                                                 slow_mo=1000,
    #                                                 channel="chrome")
    browser = await pw.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    page = await context.new_page()
    await page.goto('https://ggfw.hrss.gd.gov.cn/sydwbk/center.do?nvt=1739288858852')
    await page.click('li#Item_toDetailsPage')
    await page.click('table.datagrid-btable > tbody > tr.datagrid-row > td:nth-child(2) > div > a')
    for index in range(50):
        time.sleep(3)
        cities = await page.locator('tbody > tr.datagrid-row > td > div.datagrid-cell > a').all()
        if index >= len(cities):
            break
        city = cities[index]
        await city.click()
        while True:
            time.sleep(3)
            details = await page.locator('div.datagrid-view > div.datagrid-view2 > div.datagrid-body > table.datagrid-btable > tbody > tr.datagrid-row').all()
            for detail in details:
                message = ''
                datas = await detail.locator('div.datagrid-cell').all()
                for data in datas:
                    message += await data.text_content()
                    message += '\t'
                print(message)
            next_disable = await page.locator('body > div.index-content > div.tb_box > div.panel.datagrid > div > div.datagrid-pager.pagination > table > tbody > tr > td > a.l-btn-disabled > span > span.l-btn-icon.pagination-next').all()
            if len(next_disable) > 0:
                await page.click('#btn_return')
                break
            await page.click('body > div.index-content > div.tb_box > div.panel.datagrid > div > div.datagrid-pager.pagination > table > tbody > tr > td > a > span > span.l-btn-icon.pagination-next')


async def main():
    async with async_playwright() as playwright:
        try:
            await run(playwright)
        except Exception as e:
            print(e)

asyncio.run(main())
