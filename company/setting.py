#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： zhizhi
# datetime： 2023-08-14 14:19 
# ide： PyCharm
"""
配置文件
"""
import pathlib


class Setting:
    def __init__(self):
        # 相对路径
        self.certRecord_path = pathlib.Path(__file__).parent
        # 爱企查cookie
        # self.aqc_cookies = 'BAIDUID=9D2C8C7624A567BC198C5B1F92CAED0A:FG=1; BIDUPSID=9D2C8C7624A567BC23D0CBB7C6B405A8; PSTM=1671872316; BDUSS=B0OWF0WTlXR3lmNy1sZmI2enN5OWFtS3RUSjAyY2QzcVJIVXNpbVRMQVp4MEprSVFBQUFBJCQAAAAAAAAAAAEAAACgNks2RWRlbl9feWFv37nSogAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABk6G2QZOhtkNT; BDUSS_BFESS=B0OWF0WTlXR3lmNy1sZmI2enN5OWFtS3RUSjAyY2QzcVJIVXNpbVRMQVp4MEprSVFBQUFBJCQAAAAAAAAAAAEAAACgNks2RWRlbl9feWFv37nSogAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABk6G2QZOhtkNT; H_WISE_SIDS=234020_131862_216847_213345_214793_110085_244713_261722_236312_256419_265881_266356_267066_265615_256302_267074_259031_268592_268030_259642_256151_269731_269831_269905_270084_256739_270460_270532_270548_271051_271019_271173_271177_271227_267659_269297_271321_271350_265825_271486_266028_270102_270442_271866_269771_271812_271939_271948_269563_269665_271254_234295_234208_271188_272224_270055_263618_267596_272365_272011_272464_272507_253022_272745_272823_272802_270141_260335_269715_273064_267560_273090_273138_273266_273234_273301_273374_273400_273382_271158_273519_270183_272818_271562_271147_273673_273705_273318_272766_264170_270185_273725_273165_274077_273931_273966_274139_269609_273917_274238_273786_273045_273594_272855_203520_274356_272319_8000070_8000107_8000131_8000140_8000143_8000150_8000161_8000163_8000175_8000179_8000186_8000190_8000203; H_WISE_SIDS_BFESS=234020_131862_216847_213345_214793_110085_244713_261722_236312_256419_265881_266356_267066_265615_256302_267074_259031_268592_268030_259642_256151_269731_269831_269905_270084_256739_270460_270532_270548_271051_271019_271173_271177_271227_267659_269297_271321_271350_265825_271486_266028_270102_270442_271866_269771_271812_271939_271948_269563_269665_271254_234295_234208_271188_272224_270055_263618_267596_272365_272011_272464_272507_253022_272745_272823_272802_270141_260335_269715_273064_267560_273090_273138_273266_273234_273301_273374_273400_273382_271158_273519_270183_272818_271562_271147_273673_273705_273318_272766_264170_270185_273725_273165_274077_273931_273966_274139_269609_273917_274238_273786_273045_273594_272855_203520_274356_272319_8000070_8000107_8000131_8000140_8000143_8000150_8000161_8000163_8000175_8000179_8000186_8000190_8000203; MCITY=-257%3A; H_PS_PSSID=39676_39712_39780_39786_39704_39796_39682_39678_39818_39835_39839; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=0h21al0hal8l20a0ag0g0g2n1imo8af1q; ZFY=5vqaqTJHMkFJwJpVnLvWyZ4b9t3SE57c:A5hg0LWvjmQ:C; BAIDUID_BFESS=9D2C8C7624A567BC198C5B1F92CAED0A:FG=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=7; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22259955687%22%2C%22first_id%22%3A%2218c2e75ad9bff7-0ddec05491d565-26031051-3686400-18c2e75ad9c1591%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%2218c2e75ad9bff7-0ddec05491d565-26031051-3686400-18c2e75ad9c1591%22%7D; log_first_time=1701589888930; log_chanel=pz; ab_sr=1.0.1_MzI3MTYwNTY2NTY3YmY5NTQxNjdjZDM5ODliNGQzYzU4YmIxY2ZhZmYwMTJjZDI3M2U4ZDE4NGNkZWI1NjBiNTAwNWNlZGZhYjViZWQzNDZhNmE1ZmY4ZDc4NTBhMzRkNmQ5N2JiYWRhYmI0M2M1Yzc3Nzg4MTQ5N2FlODIyOTc5YmJiMDFjMmFiZTllMGYyYjU3MTJiNWM1OWQzM2NmYQ==; RT="z=1&dm=baidu.com&si=874d9013-f9a3-4a4d-9da1-9c4ea1c0972f&ss=lpp4obn3&sl=1x6&tt=9bu7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3albv"; log_last_time=1701592104871'
        # self.tyc_cookies = 'HWWAFSESID=ab3802207ef8154520d; HWWAFSESTIME=1701592354641; csrfToken=gitOoKhh3pOHWXWOO3rAjsac; jsid=SEO-BAIDU-ALL-SY-000001; TYCID=82d66c7091b611eead708df137e37d13; sajssdk_2015_cross_new_user=1; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1701592357; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22307570437%22%2C%22first_id%22%3A%2218c2eced6c0f60-0fb838bf989de28-26031051-3686400-18c2eced6c1126a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThjMmVjZWQ2YzBmNjAtMGZiODM4YmY5ODlkZTI4LTI2MDMxMDUxLTM2ODY0MDAtMThjMmVjZWQ2YzExMjZhIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzA3NTcwNDM3In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22307570437%22%7D%2C%22%24device_id%22%3A%2218c2eced6c0f60-0fb838bf989de28-26031051-3686400-18c2eced6c1126a%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2213143117086%22%2C%22userId%22%3A%22307570437%22%7D; tyc-user-info-save-time=1701592385823; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzE0MzExNzA4NiIsImlhdCI6MTcwMTU5MjM4NSwiZXhwIjoxNzA0MTg0Mzg1fQ.cuKVZS3Nta6Yb8Nd_aNgFOXGOKFh-8D5aPBoTMex9FO01-GYOC1pMrKV2gZsqfiNbze8qwfYVTy992SlHIWa5g; searchSessionId=1701592389.84804381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1701592390'
        # self.tyc_cookies = 'HWWAFSESID=686d63ac4fbbd7f4ed9; HWWAFSESTIME=1705407061874; csrfToken=h8IftekNRfm4-OvvOBihPX_Z; jsid=SEO-BAIDU-ALL-SY-000001; TYCID=82d66c7091b611eead708df137e37d13; sajssdk_2015_cross_new_user=1; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1705407067; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22307570437%22%2C%22first_id%22%3A%2218c2eced6c0f60-0fb838bf989de28-26031051-3686400-18c2eced6c1126a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThjMmVjZWQ2YzBmNjAtMGZiODM4YmY5ODlkZTI4LTI2MDMxMDUxLTM2ODY0MDAtMThjMmVjZWQ2YzExMjZhIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzA3NTcwNDM3In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22307570437%22%7D%2C%22%24device_id%22%3A%2218c2eced6c0f60-0fb838bf989de28-26031051-3686400-18c2eced6c1126a%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2213143117086%22%2C%22userId%22%3A%22307570437%22%7D; tyc-user-info-save-time=1705407109338; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzE0MzExNzA4NiIsImlhdCI6MTcwNTQwNzEwOSwiZXhwIjoxNzA3OTk5MTA5fQ.OtFYhMgaA1eD81X9uiaXOo9YVYUd7J-hW1GgrmJIGPHWuXm5iMXoGMSM2vcTKP5H0VTNd-QIaAKST0bBkfJvCQ; searchSessionId=1701592389.84804381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1701592390'
        # self.tyc_cookies = 'HWWAFSESID=f21661061ee7771bb71; HWWAFSESTIME=1705411481888; csrfToken=k55QWh93jXTLAaiyeMyxf48h; jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=9b9f3dc0b47211ee8099a9d7d45a236c; sajssdk_2015_cross_new_user=1; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1705411481; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22307365598%22%2C%22first_id%22%3A%2218d1272453370-03adf7b66546b98-26001951-3686400-18d127245341239%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThkMTI3MjQ1MzM3MC0wM2FkZjdiNjY1NDZiOTgtMjYwMDE5NTEtMzY4NjQwMC0xOGQxMjcyNDUzNDEyMzkiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzMDczNjU1OTgifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22307365598%22%7D%2C%22%24device_id%22%3A%2218d1272453370-03adf7b66546b98-26001951-3686400-18d127245341239%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2218122101820%22%2C%22userId%22%3A%22307365598%22%7D; tyc-user-info-save-time=1705411522387; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODEyMjEwMTgyMCIsImlhdCI6MTcwNTQxMTUxOCwiZXhwIjoxNzA4MDAzNTE4fQ.E-eYAbH6D4u76lSOEK4dzzi4BsFZLjLhdcTTAGSHNx0fquFFzFSsf4Oz7KENe6zFpmKyT9ZQBNVmRv-CwEPDbA; searchSessionId=1701592389.84804381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1705411481'
        # self.tyc_cookies = 'HWWAFSESID=f21661061ee7771bb71; HWWAFSESTIME=1705411481888; csrfToken=k55QWh93jXTLAaiyeMyxf48h; jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=9b9f3dc0b47211ee8099a9d7d45a236c; sajssdk_2015_cross_new_user=1; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1705407067; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22307570437%22%2C%22first_id%22%3A%2218d1272453370-03adf7b66546b98-26001951-3686400-18d127245341239%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThkMTI3MjQ1MzM3MC0wM2FkZjdiNjY1NDZiOTgtMjYwMDE5NTEtMzY4NjQwMC0xOGQxMjcyNDUzNDEyMzkiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIzMDc1NzA0MzcifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22307570437%22%7D%2C%22%24device_id%22%3A%2218d1272453370-03adf7b66546b98-26001951-3686400-18d127245341239%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2213143117086%22%2C%22userId%22%3A%22307570437%22%7D; tyc-user-info-save-time=1705453608049; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzE0MzExNzA4NiIsImlhdCI6MTcwNTQ1MzYwNiwiZXhwIjoxNzA4MDQ1NjA2fQ.XQHLvR_EkAmSErjSD9qXaX1Nfs8qqPCVZebppnZfTsVbxdqAc80azpkBc-PK8AKx-DK7dYCkemMxqRuHk-Uqrg; searchSessionId=1701592389.84804381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1701592390'
        self.tyc_cookies = 'HWWAFSESID=12a705b9fe0043bcec0; HWWAFSESTIME=1705454438987; csrfToken=Dlvm4pL2KGsxioqv2uifJbm5; jsid=SEO-GOOGLE-ALL-SY-000001; TYCID=a2896b60b4d611ee90f15f9344d0d825; sajssdk_2015_cross_new_user=1; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1705407067; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22310511511%22%2C%22first_id%22%3A%2218d1501a4521bc-03d2b3183afef24-26001951-2073600-18d1501a4531165%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThkMTUwMWE0NTIxYmMtMDNkMmIzMTgzYWZlZjI0LTI2MDAxOTUxLTIwNzM2MDAtMThkMTUwMWE0NTMxMTY1IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMzEwNTExNTExIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22310511511%22%7D%2C%22%24device_id%22%3A%2218d1501a4521bc-03d2b3183afef24-26001951-2073600-18d1501a4531165%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2218613097737%22%2C%22userId%22:%22310511511%22}; tyc-user-info-save-time=1705454771579; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODYxMzA5NzczNyIsImlhdCI6MTcwNTQ1NDc3MCwiZXhwIjoxNzA4MDQ2NzcwfQ.zk-5yXhQmAnsuyN1EhDctwVDmHgSI2-yR9sL4Ykg3y0OGNsJmhNVgP5YdKIds8pIdNxcRbq-FCeyyEZlagqseg; searchSessionId=1701592389.84804381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1701592390'

        # 企查查cookie
        # self.qcc_cookies = ''


settings = Setting()