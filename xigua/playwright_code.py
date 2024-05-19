import random
import time
import json
import xiGuaInfo
import pandas as pd

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
search_position = "广东"
data_all = []


def run(pw: Playwright, index: str) -> None:
    try:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )

        context.add_cookies(cookie)
        page = context.new_page()
        page.goto("https://data.xiguaji.com/Home#/staticpage/officialSearch")

        flag = True
        total = 0
        page_index = 1
        error = 0
        while(flag):
            result = page.request.post(url="https://data.xiguaji.com/v2/biz/Search?_=" + str(int(round(time.time() * 1000))),
                              data={"pageIndex": page_index, "pageSize": page_size, "BizSort": 6, "Industry": "10", "Position": search_position})

            if result.status == 200:
                json_result = result.body()
                data = json.loads(json_result.decode('utf8'))
                if data['Code'] == 200:
                    count = data['Data']['TotalCount']
                    list = data['Data']['ItemList']
                    total += len(list)
                    data_all.extend(list)
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
            df.to_excel('西瓜数据_公众号_' + search_position + '_' + str(len(data_all)) + '_' + time_now + '.xlsx', index=False)
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
