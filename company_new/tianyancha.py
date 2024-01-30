#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： zhizhi
# datetime： 2023-08-14 10:37
# ide： PyCharm
"""
天眼查查询类
利用天眼查网站收集资产信息
https://www.tianyancha.com
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from company_new.companyInfo import CompanyInfoBase
from setting import settings
import random


class Tianyancha:
    """
    天眼查企业查询类
    """
    def __init__(self):
        self.url = "https://www.tianyancha.com"
        self.options = webdriver.EdgeOptions()
        self.source = 'tianyancha'
        self.driver = None

    def int_driver(self):
        """
        初始化浏览器设置
        :return:
        """
        # logger.log('INFOR', '正在使用天眼查网站获取企业资产信息')
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/94.0.4606.71 Safari/537.36')  # 添加请求头
        self.options.add_argument('headless')  # 设置后台运行
        self.options.add_argument('window-size=1920x1080')  # 设置浏览器显示大小
        self.options.add_argument('start-maximized')  # 最大显示
        self.options.add_argument('--disable-blink-features=AutomationControlled')  # 避免被检测
        self.driver = webdriver.Edge(options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})

        # 隐藏指纹特征
        min_path = 'stealth.min.js'
        with open(min_path) as f:
            js = f.read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

    def int_home(self):
        """
            获取企业的主页面
        """
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.delete_all_cookies()
        self.add_cookies()  # 加载cookies
        self.driver.maximize_window()  # 最大化浏览器窗口

    def quit_driver(self):
        """
        关闭浏览器
        :return:
        """
        if self.driver is not None:
            self.driver.quit()

    """
        添加cookies, self.driver.add_cookie(cookies)添加cookies时要求其必须有name和value字段
        具体可参考https://blog.csdn.net/qew110123/article/details/115335490
        :return:
    """
    def add_cookies(self):
        cookies_list = settings.tyc_cookies.split()  # 按空格分割
        for i in cookies_list:
            name, value = i.strip().split("=", 1)
            cookies = {'name': name, 'value': value[:-1] if value.endswith(";") else value}
            self.driver.add_cookie(cookies)
        self.driver.refresh()  # 自动刷新页面，请检查是否已经自动登录账号

    def search(self, name, company):
        self.driver.get(self.url + f'/search?key={name}')  # 搜索特定企业
        time.sleep(random.uniform(1, 2))
        id_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div.index_header__x2QZ3 > div.index_name__qEdWi > a")
        search_name_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div.index_header__x2QZ3 > div.index_name__qEdWi > a > span")
        human_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div.index_info-row__xbtyD.index_line-row__R3mCi > div.index_info-col__UVcZb.index_wider__gQok0 > a")
        money_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div.index_info-row__xbtyD.index_line-row__R3mCi > div.index_info-col__UVcZb.index_narrow__QeZfV > span")
        create_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div.index_info-row__xbtyD.index_line-row__R3mCi > div:nth-child(3) > span")
        tel_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div:nth-child(4) > div:nth-child(1) > span:nth-child(2) > span")
        email_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div:nth-child(4) > div:nth-child(2) > span:nth-child(2)")
        address_list = self.driver.find_elements(By.CSS_SELECTOR, "#page-container > div > div.index_search-main__4nIOp > section > main > div.index_search-list-wrap__wi3T0 > div.index_list-wrap___axcs > div:nth-child(1) > div > div.index_search-item__W7iG_ > div.index_search-item-center__Q2ai5 > div:nth-child(5) > div > span:nth-child(2)")

        if len(id_list) <= 0:
            return None

        id = id_list[0].get_attribute("href").split("/")[-1]
        search_name, human, money, create, tel, email, address = '暂无数据', '暂无数据', '暂无数据', '暂无数据', '暂无数据', '暂无数据', '暂无数据'
        if len(search_name_list) > 0:
            search_name = search_name_list[0].text
        if len(human_list) > 0:
            human = human_list[0].text
        if len(money_list) > 0:
            money = money_list[0].text
        if len(create_list) > 0:
            create = create_list[0].text
        if len(tel_list) > 0:
            tel = tel_list[0].text
        if len(email_list) > 0:
            email = email_list[0].text
        if len(address_list) > 0:
            address = address_list[0].text
        return CompanyInfoBase(id, search_name, human, money, create, tel, email, address, company)


