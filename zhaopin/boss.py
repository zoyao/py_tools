import time

from playwright.sync_api import Playwright, sync_playwright
from all import info, job_name_search, job_name_ignore, company, company_ignore

urls = ['https://www.zhipin.com/web/geek/job?city=101280100&query=', 'https://www.zhipin.com/web/geek/job?city=101280800&query=']
domain = 'https://www.zhipin.com'


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
        for i in range(50):
            page.goto(url + info + '&page=' + str(i + 1))
            for j in range(10):
                list = page.locator('#wrap > div.page-job-wrapper > div.page-job-inner > div > div.job-list-wrapper > div.search-job-result > ul > li > div.job-card-body.clearfix').all()
                if len(list) < 10:
                    time.sleep(1)
                else:
                    break
            for item in list:
                job_name = item.locator('div.job-title.clearfix > span.job-name').inner_text()
                address = item.locator('a > div.job-title.clearfix > span.job-area-wrapper > span.job-area').inner_text()
                company_name = item.locator('div > div.company-info > h3 > a').inner_text()
                salary = item.locator('a > div.job-info.clearfix > span.salary').inner_text()
                tag = item.locator('a > div.job-info.clearfix > ul').inner_text().replace('\n', ' ')
                for job_urls in item.locator('a.job-card-left').all():
                    job_url = domain + job_urls.get_attribute('href')
                    if '/job_detail/' in job_url:
                        break
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
