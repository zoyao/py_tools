from notice_tool.pushdeer import send_notice
from common.log import logging
from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
from check_tool.check import check
from config.config import conf


class ElementY(object):
    def __init__(self, absolute_links, text):
        self.absolute_links = absolute_links
        self.text = text


class lukou(object):
    session = HTMLSession()

    def __init__(self, config=conf()):
        self.end_id = 0
        self.config = config

    def login(self):
        logging.info('login')
        self.session.post('https://www.lukou.com/login?type=phone&password=clock668204y&phone=13143117086')

    def check(self):
        logging.info('begin')
        begin_end_id = self.end_id
        first_flag = True
        result = self.session.get('https://www.lukou.com/circle')
        if not result.html.find('.feedlist'):
            self.login()
            result = self.session.get('https://www.lukou.com/circle')
        start = 10
        page = 0
        while True:
            base_url = 'https://www.lukou.com/service/feeds'
            start += 10
            if type(result) == str:
                # 兼容下拉加载数据，下拉数据以json方式返回
                soup = BeautifulSoup(result, 'html.parser')
                soup_list = soup.findAll('div', class_='feed-wrap')
                list = []
                for soup_x in soup_list:
                    text = soup_x.text
                    url_list = soup_x.findAll('a')
                    absolute_links = []
                    for u in url_list:
                        url = u.attrs.get('href')
                        if url:
                            absolute_links.append(url)
                    x = ElementY(absolute_links, text)
                    list.append(x)
            else:
                # 获取页面数据
                list = result.html.find('.feed-wrap')
            for x in list:
                for url in x.absolute_links:
                    if 'lukou' in url and 'userfeed' in url and '#' not in url:
                        break
                # 根据url读取商品id
                if '?' in url:
                    id_str = url[url.index('userfeed/') + 9:url.index('?')]
                else:
                    id_str = url[url.index('userfeed/') + 9:]
                logging.info(id_str)
                try:
                    id = int(id_str)
                except Exception as e:
                    id = 0
                    logging.error(url)
                    logging.error(x.absolute_links)
                if id <= begin_end_id:
                    # 已读取过商品，直接退出
                    logging.info('end')
                    return
                if first_flag:
                    # 记录第一个商品的id，后续下拉获取及翻页接口需要
                    first_flag = False
                    end_id = id
                    if end_id > self.end_id:
                        self.end_id = end_id
                detail = x.text
                # auth = x.find('.author')
                words = '【无】'
                # 检查是否有匹配内容
                for c in self.config.get_check_list():
                    user = c['user']
                    flag = check(c, detail)
                    if flag:
                        # 调用通知接口
                        send_notice(user, '路口关键词匹配成功' + words, detail + '<' + url + '>', self.config)
            format_flag = True
            if start >= 50:
                # 翻页
                start = 10
                page += 1
                base_url = 'https://www.lukou.com/circle'
                format_flag = False
            if page >= 5:
                logging.info('end')
                return
            result = self.session.get(base_url + '?end_id=' + str(end_id) + '&page=' + str(page) + '&start=' + str(start))
            if format_flag:
                # 兼容下拉加载数据，下拉数据以json方式返回
                result = json.loads(result.html.html).get('html')
