import random
import time
import json
import pandas as pd
from itertools import product
import xiGuaInfo

from playwright.sync_api import Playwright, sync_playwright, expect


cookie = [
{
    "domain": ".data.xiguaji.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "Hm_lpvt_91a409c98f787c8181d5bb8ee9c535ba",
    "path": "/",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "1716087978",
    "id": 1
},
{
    "domain": ".data.xiguaji.com",
    "expirationDate": 1747623977,
    "hostOnly": False,
    "httpOnly": False,
    "name": "Hm_lvt_91a409c98f787c8181d5bb8ee9c535ba",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "1716085966",
    "id": 2
},
{
    "domain": ".data.xiguaji.com",
    "expirationDate": 1716173401.602724,
    "hostOnly": False,
    "httpOnly": False,
    "name": "XIGUADATA",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "UserId=47e4b3cbac6aac75&checksum=1d4a9e8c3e5e&ChildUserId=d80c3b980d33ea5f&XIGUADATALIMITID=80d5afc9912a4989857368dccd805932&LvId=4c2d06c3ad4dbc85a1d43bb471ec5ef243dc4ab1aa1baf41",
    "id": 3
},
{
    "domain": ".xiguaji.com",
    "expirationDate": 1731638999,
    "hostOnly": False,
    "httpOnly": False,
    "name": "tfstk",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "fLxo_LNUfU7S6_yKZnjS0mH2sTgAV7sCrBEd9MCEus5XvY1KPE2ewCa-FeLJo6A2i_RHdY6FTBRh9U3xXL95AMlOxcn9FSDEU1dlLToqL9WOLPs3CLJ5AMlx-7lNNLOMqBejZMkc09XlLM7FLrkcpOXPY_7UgrWNg6SFYB7409WTzyrFaKSqN84P6H8w0A3_sJJyu3-cEZuvUsuvtnWlz1JyqkreQTbl_L5m6vr39ZJC-HwQxw9y5B6wa7lOPp8DiTjnDzSwneRGh3oTZtTJ3B12IJqHegxDme7mU0Jcq_bGeN2LPgYeNHbWrJM63gRX51_rlj6D2hQh1ZVqaKpcaNYHwjZFwFv2iNKYMlIBGeRFKIPl4az47X_YANcWSyaCzt6c1j8O__hQwZdinx49daWfC1HmnyOczt6jbxD07k7PhTtA.",
    "id": 4
},
{
    "domain": ".xiguaji.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "UserUnionId",
    "path": "/",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "",
    "id": 5
},
{
    "domain": ".xiguaji.com",
    "expirationDate": 1716173401.602724,
    "hostOnly": False,
    "httpOnly": False,
    "name": "XIGUADATA",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "UserId=47e4b3cbac6aac75&checksum=1d4a9e8c3e5e&ChildUserId=d80c3b980d33ea5f&XIGUADATALIMITID=80d5afc9912a4989857368dccd805932&LvId=4c2d06c3ad4dbc85a1d43bb471ec5ef243dc4ab1aa1baf41",
    "id": 6
},
{
    "domain": "data.xiguaji.com",
    "expirationDate": 1747313865.310453,
    "hostOnly": True,
    "httpOnly": False,
    "name": "_data_chl",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "key=BaiduOrginal",
    "id": 7
},
{
    "domain": "data.xiguaji.com",
    "expirationDate": 1747313865.817611,
    "hostOnly": True,
    "httpOnly": False,
    "name": "_uab_collina",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "171275386582707061796014",
    "id": 8
},
{
    "domain": "data.xiguaji.com",
    "hostOnly": True,
    "httpOnly": True,
    "name": "ASP.NET_SessionId",
    "path": "/",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "14dacegzsebfzv53fpv1pgny",
    "id": 9
},
{
    "domain": "data.xiguaji.com",
    "hostOnly": True,
    "httpOnly": False,
    "name": "compareArray",
    "path": "/",
    "secure": False,
    "session": True,
    "storeId": "0",
    "value": "[]",
    "id": 10
},
{
    "domain": "data.xiguaji.com",
    "expirationDate": 1718679001,
    "hostOnly": True,
    "httpOnly": False,
    "name": "SaveUserName",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "18122101820",
    "id": 11
},
{
    "domain": "data.xiguaji.com",
    "expirationDate": 1716346202,
    "hostOnly": True,
    "httpOnly": False,
    "name": "systemupdatenotice",
    "path": "/",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "147",
    "id": 12
}
]
page_size = 50
search_position = "山东"
# City_list = [None, '广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市',
#              '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '佛山市', '云浮市']
# City_list = [None, '南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市',
#              '泰州市', '宿迁市']
City_list = [None, '济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市',
             '莱芜市', '临沂市', '德州市', '聊城市', '滨州市', '菏泽市']
data_all = []
data_set = set()
max_size = 0
# 预计活粉
Fans_list = [None, 1, 2, 3, 4, 5, 6]
# 平均阅读
Read_list = [None, 1, 2, 3, 4, 5, 6]
# 30天广告
MonthAdArticleCount_list = [None, 0, 1, 2, 3, 4]
# 近期发文
LastPubDay_list = [None, 3, 7, 30, 60, 90]
# 西瓜指数
GuaZhiShu_list = [None, 1, 2, 3, 4, 5]
# 男女比例
# Ratio_list = [None, 1, 2]
Ratio_list = [None]
# 营运主体p
# CustomerType_list = [None, 0, 1, 2, 3, 4]
CustomerType_list = [None]
# 注册时间
# Register_list = [None, 4, 5, 6, 7, 8]
Register_list = [None]
# 原创号
# original_list = [None, 1]
original_list = [None]
# 服务号
# IsService_list = [None, 1]
IsService_list = [None]
# 带视频内容
# IsChannalsBiz_list = [None, 1]
IsChannalsBiz_list = [None]
# 微信视频号
# IsVideo_list = [None, 1]
IsVideo_list = [None]
# 有投前分析
# IsTracking_list = [None, 1]
IsTracking_list = [None]
# 有涉及小程序
# IsHasMiniApp_list = [None, 1]
IsHasMiniApp_list = [None]
# 互选广告
# IsHuXuan_list = [None, 1]
IsHuXuan_list = [None]
# 结果排序
BizSort_list = [None, 1, 2, 3, 4, 5, 6, 7, 8]
# 排列组合
loop_list = [Fans_list, Read_list, MonthAdArticleCount_list, LastPubDay_list, GuaZhiShu_list, Ratio_list,
             CustomerType_list, Register_list, original_list, IsService_list, IsChannalsBiz_list, IsVideo_list,
             IsTracking_list, IsHasMiniApp_list, IsHuXuan_list, BizSort_list, City_list]



def run(pw: Playwright, index: str) -> None:
    try:
        params_list = set()
        loop_list = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], City_list]
        for params in product(*loop_list):
            if not params_list.__contains__(params):
                params_list.add(params)
        loop_list = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None],
                     [None], [None], [None], BizSort_list, [None]]
        for params in product(*loop_list):
            if not params_list.__contains__(params):
                params_list.add(params)
        loop_list = [Fans_list, [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None],
                     [None], [None], [None], BizSort_list, [None]]
        for params in product(*loop_list):
            if not params_list.__contains__(params):
                params_list.add(params)
        loop_list = [[None], Read_list, [None], [None], [None], [None], [None], [None], [None], [None], [None], [None],
                     [None], [None], [None], BizSort_list, [None]]
        for params in product(*loop_list):
            if not params_list.__contains__(params):
                params_list.add(params)

        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )

        context.add_cookies(cookie)
        page = context.new_page()
        page.goto("https://data.xiguaji.com/Home#/staticpage/officialSearch")
        global max_size

        for params in params_list:
            flag = True
            page_index = 1
            error = 0
            total = 0
            while(flag):
                Fans = params[0]
                Read = params[1]
                MonthAdArticleCount = params[2]
                LastPubDay = params[3]
                GuaZhiShu = params[4]
                Ratio = params[5]
                CustomerType = params[6]
                Register = params[7]
                original = params[8]
                IsService = params[9]
                IsChannalsBiz = params[10]
                IsVideo = params[11]
                IsTracking = params[12]
                IsHasMiniApp = params[13]
                IsHuXuan = params[14]
                BizSort = params[15]
                City = params[16]

                data = {
                    "pageIndex": page_index,
                    "pageSize": page_size,
                    "Industry": "10",
                    "Position": search_position,
                    "Fans": Fans,
                    "Read": Read,
                    "MonthAdArticleCount": MonthAdArticleCount,
                    "LastPubDay": LastPubDay,
                    "GuaZhiShu": GuaZhiShu,
                    "Ratio": Ratio,
                    "CustomerType": CustomerType,
                    "Register": Register,
                    "original": original,
                    "IsService": IsService,
                    "IsChannalsBiz": IsChannalsBiz,
                    "IsVideo": IsVideo,
                    "IsTracking": IsTracking,
                    "IsHasMiniApp": IsHasMiniApp,
                    "IsHuXuan": IsHuXuan,
                    "BizSort": BizSort,
                    "City": City
                }
                data = {k: v for k, v in data.items() if v is not None}
                result = page.request.post(url="https://data.xiguaji.com/v2/biz/Search?_=" + str(int(round(time.time() * 1000))),
                                  data=data)

                if result.status == 200:
                    json_result = result.body()
                    data = json.loads(json_result.decode('utf8'))
                    if data['Code'] == 200:
                        count = data['Data']['TotalCount']
                        if count > max_size:
                            max_size = count
                        list = data['Data']['ItemList']
                        total += len(list)
                        for item in list:
                            id = item['BizId']
                            if not data_set.__contains__(id):
                                data_set.add(id)
                                data_all.append(item)
                        # for item in list:
                        #     info = xiGuaInfo.XiGuaInfo(item)
                        #     print(info)
                        page_index += 1
                        if total >= count:
                            flag = False
                    else:
                        error += 1
                else:
                    error += 1

                if error > 10:
                    break
                time.sleep(random.randint(3, 5))
    except Exception as e:
        print(e)
    finally:
        time_now = time.strftime('%Y%m%d%H%M%S', time.localtime())
        if len(data_all) > 0:
            df = pd.json_normalize(data_all)
            df.to_excel('西瓜数据_公众号_' + search_position + '_总' + str(max_size) + '_' + str(len(data_all)) + '_' +
                        time_now + '.xlsx', index=False)
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
    index = str(int(round(time.time() * 1000))) + '_'
    for i in range(1):
        if i > 0:
            time.sleep(random.randint(20, 100))
        try:
            run(playwright, index + str(i))
        except Exception as e:
            print(e)
