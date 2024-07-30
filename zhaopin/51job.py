import time

from playwright.sync_api import Playwright, sync_playwright
import json
from all import info, job_name_search, job_name_ignore, company, company_ignore


urls = ['https://we.51job.com/pc/search?jobArea=030200&keyword=', 'https://we.51job.com/pc/search?jobArea=030600&keyword=']
domain = 'https://jobs.51job.com/job/'


def run(pw: Playwright, info: str, job_name_search: list, job_name_ignore: list, company: list, company_ignore: list):
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={'width': 600, 'height': 1000}
    )

    page = context.new_page()
    page.set_default_timeout(120000)
    page_info = context.new_page()
    page_info.set_default_timeout(120000)
    job_list = []
    job_list_no_ingore = []

    for url in urls:
        page.goto(url + info)
        for i in range(50):
            for j in range(10):
                list = page.locator('div.joblist > div.joblist-item > div > div').all()
                if len(list) < 10:
                    time.sleep(1)
                else:
                    break
            for item in list:
                job_name = item.locator('div.joblist-item-top > span.jname').inner_text()
                address = item.locator('div.joblist-item-bot > div.br > div.area > div').inner_text()
                company_name = item.locator('div.joblist-item-bot > div.bl > a.cname').inner_text()
                salary = item.locator('div.joblist-item-top > span.sal').inner_text()
                tag = ''
                sensorsdata = item.get_attribute("sensorsdata")
                sensorsdata_json = json.loads(sensorsdata)
                job_url = domain + sensorsdata_json['jobId'] + '.html'
                company_flag = False
                if (company is None):
                    company_flag = True
                else:
                    for c in company:
                        if c in company_name:
                            company_flag = True
                            break
                if company_flag and company_ignore is not None:
                    for c in company_ignore:
                        if c in company_name:
                            company_flag = False
                            break
                if company_flag:
                    text = company_name + '\t' + job_name + '\t' + address + '\t' + salary + '\t' + tag + '\t' + job_url
                    job_name_flag = False
                    if job_name_search is None:
                        job_name_flag = True
                    else:
                        for io in job_name_search:
                            if io in job_name:
                                job_name_flag = True
                                break
                    if job_name_flag:
                        print('匹配\t' + text)
                        job_list.append(text)

                    job_name_flag = True
                    if job_name_ignore is not None:
                        for ig in job_name_ignore:
                            if ig in job_name:
                                job_name_flag = False
                                break
                    if job_name_flag:
                        print('疑似\t' + text)
                        job_list_no_ingore.append(text)
            btn_list = page.locator('div.bottom-page > div > div.pageation > div > button.btn-next').all()
            if len(btn_list) > 0:
                btn = btn_list[0]
                if not btn.is_disabled():
                    btn.click()
            else:
                break
            time.sleep(2)
    print('匹配岗位：')
    for job in job_list:
        print(job)
    print('疑似岗位：')
    for job in job_list_no_ingore:
        print(job)
    return job_list, job_list_no_ingore


with sync_playwright() as playwright:
    try:
        run(playwright, info, job_name_search, job_name_ignore, company, company_ignore)
    except Exception as e:
        print(e)
