from selenium import webdriver
import os
import yaml
from selenium.webdriver.common.by import By
from notice_tool import notice
import time


class lukou(object):
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')  # 设置option
    option.add_argument('--disable-dev-shm-usage')  # 设置option
    option.add_argument('--headless')  # 设置option
    option.add_argument('blink-settings=imagesEnabled=false')  # 设置option
    option.add_argument('--disable-gpu')  # 设置option
    browser = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器
    check_list = []
    end_id = 0

    def __init__(self):
        with open(os.path.expanduser("../config/config.yaml"), "r", encoding='utf-8') as config:
            cfg = yaml.safe_load(config)
            self.check_list = cfg['check']['lukou']['list']

    def login(self):
        self.browser.get('https://www.lukou.com/?login')
        self.browser.find_element(By.CSS_SELECTOR, '.login').click()
        self.browser.find_element(By.CSS_SELECTOR, '#email').send_keys('13143117086')
        self.browser.find_element(By.CSS_SELECTOR, '#password').send_keys('clock668204y')
        self.browser.find_element(By.CSS_SELECTOR, '#loginSubmit').click()
        time.sleep(3)

    def reload(self, times=1):
        for i in range(times):
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)

    def check(self):
        begin_end_id = self.end_id
        first_flag = True
        self.browser.get('https://www.lukou.com/circle')
        list = self.browser.find_elements(By.CSS_SELECTOR, '.feed-wrap')
        #login
        if (not list):
            print('login')
            self.login()
        #get all
        circle_url = 'https://www.lukou.com/circle'
        url = circle_url
        page = 0
        while True:
            self.browser.get(url)
            self.reload(7)
            list = self.browser.find_elements(By.CSS_SELECTOR, '.feed-wrap')
            if (not list):
                return
            for x in list:
                url = x.find_element(By.CSS_SELECTOR, '.feed-link').get_attribute('href')
                if '?' in url:
                    id_str = url[url.index('userfeed/') + 9:url.index('?')]
                else:
                    id_str = url[url.index('userfeed/') + 9:]
                id = int(id_str)
                if id <= begin_end_id:
                    return
                if first_flag:
                    first_flag = False
                    end_id = id
                    if end_id > self.end_id:
                        self.end_id = end_id
                detail = x.text
                # auth = x.find('.author')
                words = '【无】'
                for c in self.check_list:
                    user = c['user']
                    flag = False
                    if 'keywords' in c.keys():
                        for keys in c['keywords']:
                            words = ''
                            key_flag = True
                            for key in keys.split(','):
                                words += '【' + key + '】'
                                if key not in detail:
                                    key_flag = False
                                    break
                            if key_flag:
                                flag = True
                                break
                    else:
                        flag = True
                    if flag:
                        notice.send_notice(user, '路口关键词匹配成功' + words, detail + '<' + url + '>')
            page += 1
            url = circle_url + '?end_id=' + str(end_id) + '&page=' + str(page)
            if page >= 5:
                return