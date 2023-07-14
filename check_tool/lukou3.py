import os
import yaml
from notice_tool.pushdeer import notice
from common.log import logging
from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup


class ElementY(object):
    def __init__(self, absolute_links, text):
        self.absolute_links = absolute_links
        self.text = text


class lukou(object):
    session = HTMLSession()

    def __init__(self, base_dir='..'):
        self.check_list = []
        self.end_id = 0
        self.notice = notice(base_dir)
        with open(os.path.expanduser(base_dir + "/config/config.yaml"), "r", encoding='utf-8') as config:
            cfg = yaml.safe_load(config)
            self.check_list = cfg['check']['lukou']['list']

    def login(self):
        logging.info('login')
        self.session.post('https://www.lukou.com/login?type=phone&password=clock668204y&phone=13143117086')

    def check(self):
        logging.info('begin')
        begin_end_id = self.end_id
        first_flag = True
        result = self.session.get('https://www.lukou.com/circle')
        if (not result.html.find('.feedlist')):
            self.login()
            result = self.session.get('https://www.lukou.com/circle')

        start = 10
        page = 0
        while True:
            base_url = 'https://www.lukou.com/service/feeds'
            start += 10
            if type(result) == str:
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
                list = result.html.find('.feed-wrap')
            for x in list:
                for url in x.absolute_links:
                    if 'lukou' in url and 'userfeed' in url and '#' not in url:
                        break
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
                    logging.info('end')
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
                        self.notice.send_notice(user, '路口关键词匹配成功' + words, detail + '<' + url + '>')
            format_flag = True
            if start >= 50:
                start = 10
                page += 1
                base_url = 'https://www.lukou.com/circle'
                format_flag = False
            if page >= 5:
                logging.info('end')
                return
            result = self.session.get(base_url + '?end_id=' + str(end_id) + '&page=' + str(page) + '&start=' + str(start))
            if format_flag:
                result = json.loads(result.html.html).get('html')
