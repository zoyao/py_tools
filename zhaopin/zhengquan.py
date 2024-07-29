import time

from playwright.sync_api import Playwright, sync_playwright


def run(pw: Playwright) -> None:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 600, 'height': 1000}
    )

    url = 'http://www.yinhangzhaopin.com/zqgszp/list_2273_'
    url_info = 'http://www.yinhangzhaopin.com'
    page = context.new_page()
    page.set_default_timeout(120000)
    page_info = context.new_page()
    page_info.set_default_timeout(120000)

    flag = False
    for i in range(9):
        page.goto(url + str(i + 1) + '.html')
        list = page.locator('#midder > div.ll > div > div.bd > dl > dt > a').all()
        for item in list:
            href = url_info + item.get_attribute('href')
            title = item.get_attribute('title')
            if flag:
                page_info.goto(href)
                html = page_info.locator('#midder > div.ll > div.side-1 > div.bd > div > div.newstxt').inner_html()
                if '广州' in html or '佛山' in html:
                    print(title + '\t' + href)
                time.sleep(2)
            if href == 'http://www.yinhangzhaopin.com/zqgszp/5/166715.htm':
                flag = True
    time.sleep(2)


with sync_playwright() as playwright:
    try:
        run(playwright)
    except Exception as e:
        print(e)
