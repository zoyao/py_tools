#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： zhizhi
# datetime： 2023-08-15 9:33 
# ide： PyCharm
from tianyancha import Tianyancha
import pandas as pd


def print_info(info):
    print(info.name + '\t' + info.tel)

if __name__ == '__main__':
    path = 'szsm1.xlsx'
    data = pd.read_excel(path, sheet_name='Sheet1')
    modu = Tianyancha()  # 创建天眼查查询类
    flag = True
    for company in data.values:
        try:
            if flag:
                modu.quit_driver()
                modu.int_driver()  # 初始化浏览器设置
                modu.int_home()
            flag = False
            name = company[1]
            name.replace('*', '')
            base = modu.search(name)
            if base is None:
                print('error')
                continue

            name_fix = name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
            search_name_fix = base.name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
            if name_fix == search_name_fix:
                print_info(base)
            else:
                base2 = modu.search(name)
                if base == base2:
                    print_info(base)
                else:
                    search_name_fix2 = base2.name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
                    if name_fix == search_name_fix2:
                        print_info(base2)
                    else:
                        base3 = modu.search(name)
                        print_info(base3)
        except Exception as e:
            print('error')
            print(e)
            flag = True
    modu.quit_driver()  # 关闭浏览
    print(1)
