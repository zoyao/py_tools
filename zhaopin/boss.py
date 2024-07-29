import time

from playwright.sync_api import Playwright, sync_playwright


urls = ['https://www.zhipin.com/web/geek/job?city=101280100&query=', 'https://www.zhipin.com/web/geek/job?city=101280800&query=']
info = '证券'
job_name_search = ['后台', '柜台', '柜员', '综合', '合规', '开户', '人事']
job_name_ignore = ['实习', '经纪', '投顾', '顾问', '客户', '总经理', '负责人', '总监', '理财', '工程', '讲师', '产品', '运营',
                   '运维', '营销', '分析', '证券从业人员', '培训', '渠道', '证券经理', '业务经理', '项目经理', '投资咨询']
company = '证券'
domain = 'https://www.zhipin.com'

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
    job_list = []
    job_list_no_ingore = []

    flag = False
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
                if company is None or company in company_name:
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


with sync_playwright() as playwright:
    try:
        run(playwright)
    except Exception as e:
        print(e)
