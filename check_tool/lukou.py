from requests_html import HTMLSession
import os
import yaml
from notice_tool.pushdeer import notice


class lukou(object):
    session = HTMLSession()
    check_list = []
    end_id = 0

    def __init__(self):
        with open(os.path.expanduser("../config/config.yaml"), "r", encoding='utf-8') as config:
            cfg = yaml.safe_load(config)
            self.check_list = cfg['check']['lukou']['list']

    def check(self):
        begin_end_id = self.end_id
        first_flag = True
        result = self.session.get('https://www.lukou.com/circle')
        if (not result.html.find('.feedlist')):
            print('login')
            self.session.post('https://www.lukou.com/login?type=phone&password=clock668204y&phone=13143117086')
            result = self.session.get('https://www.lukou.com/circle')
        # result.html.render()
        # result.html.render(scrolldown=1)
        result.html.render(scrolldown=4, sleep=2)

        start = 10
        page = 0
        while True:
            start += 10
            list = result.html.find('.feed-wrap')
            for x in list:
                for url in x.absolute_links:
                    if 'lukou' in url and 'userfeed' in url and \
                            ('#comments' in url or '?refererId=moment' in url):
                        break
                id = int(url.replace('http://www.lukou.com/userfeed/', '').replace('#comments', '').replace('?refererId=moment', ''))
                if id <= begin_end_id:
                    return
                if first_flag:
                    first_flag = False
                    end_id = id
                    if end_id > self.end_id:
                        self.end_id = end_id
                detail = x.text
                auth = x.find('.author')
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
            if start >= 50:
                start = 10
                page += 1
            if page >= 5:
                return
            result.html.page.keyboard.down('PageDown')
            # json = self.session.get('https://www.lukou.com/service/feeds?end_id=' + str(end_id) + '&page='
            #                           + str(page) + '&start=' + str(start)).html
            print(1)

lu = lukou()
lu.check()