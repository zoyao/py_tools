import random
import time

import pymysql

from playwright.sync_api import Playwright, sync_playwright, expect

domain = 'https://yz.chsi.com.cn'
url = '/zsml/dw.do'


def run(pw: Playwright) -> None:
    try:
        browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]  # 注意这里不是browser.new_page()了
        page = context.new_page()
        page_school = context.new_page()
        page.goto(domain + url)
        for area in page.locator("div.area-list > div:nth-child(18)").all():
            if '广东' == area.inner_text():
                area.click()
        for option in page.locator("div.options > div > label:nth-child(2)").all():
            if '全日制' == option.inner_text():
                option.click()
        while True:
            time.sleep(1)
            for school in page.locator('div.zy-list > div > div.yx-right > a.zy-btn.ivu-btn.ivu-btn-primary').all():
                page_school.goto(domain + school.get_attribute('href'))
                school_name = page_school.locator('div.yx-detail > div.yx-name').first.inner_text()
                while True:
                    for major in page_school.locator(
                            'div.detail-yx-list.zy-list > div.zy-item').all():
                        if major.inner_text().__contains__('专业学位'):
                            major_name = major.locator('div.yx-total-info > div.zy-info > div.zy-name').first.inner_text()
                            major_name = major_name.replace('\n', '\t')
                            major.locator('div.yx-total-info > div.yx-right > a.show-more').first.click()
                            time.sleep(random.randint(2, 3))
                            members = major.locator('div.ivu-tooltip-popper.ivu-tooltip-dark > div.ivu-tooltip-content > div.ivu-tooltip-inner.ivu-tooltip-inner-with-width').first.inner_text()
                            for direction in major.locator(
                                    'div.ivu-table-body > table > tbody.ivu-table-tbody > tr.ivu-table-row').all():
                                direction_name = ''
                                for cell in direction.locator('div.ivu-table-cell > div.ivu-table-cell-slot').all():
                                    cell_name = cell.inner_text()
                                    if len(cell_name) > 0 and cell_name not in ['是', '否', '查看', '详情 对比']:
                                        direction_name += cell.inner_text() + '\t'
                                for direction_need in direction.locator(
                                        'div.kskm-modal.kskm-detail-list > div.kskm-item').all():
                                    item_name = ''
                                    for item in direction_need.locator('div.kskm-detail > div.item').all():
                                        item_html = item.inner_html()
                                        item_html = item_html.split('<span>')[0]
                                        item_name += item_html + '\t'
                                    print(school_name + '\t' + major_name + '\t' + direction_name + item_name + members)
                            major.locator('div.yx-total-info > div.yx-right > a.show-more').first.click()
                            time.sleep(random.randint(1, 2))
                    time.sleep(random.randint(1, 5))
                    if len(page_school.locator(
                            'div.margin-top-20.clearfix > ul > li.ivu-page-next.ivu-page-disabled > a').all()) > 0:
                        break
                    if len(page_school.locator('div.margin-top-20.clearfix > ul > li.ivu-page-next > a').all()) <= 0:
                        break
                    page_school.locator('div.margin-top-20.clearfix > ul > li.ivu-page-next > a').first.click()
                    time.sleep(random.randint(2, 4))
            if len(page.locator('div.margin-top-20.clearfix > ul > li.ivu-page-next.ivu-page-disabled > a').all()) > 0:
                break
            if len(page.locator('div.margin-top-20.clearfix > ul > li.ivu-page-next > a').all()) <= 0:
                break
            page.locator('div.margin-top-20.clearfix > ul > li.ivu-page-next > a').first.click()
    except Exception as e:
        print(e)
    finally:
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
