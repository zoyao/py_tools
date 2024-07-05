#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： zhizhi
# datetime： 2023-08-15 9:33 
# ide： PyCharm
import time

import numpy as np

from tianyancha import Tianyancha
import pandas as pd

excel_file = 'output.xlsx'
start_row = 1

def print_info(info, status):
    info.status = status
    df = pd.DataFrame([vars(info)])
    global start_row
    with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, startrow=start_row, header=False)
    start_row = start_row + 1
    print(info.name + '\t' + info.tel + '\t' + info.human + '\t' + info.email + '\t' + info.address + '\t' + str(status))

if __name__ == '__main__':
    df = pd.DataFrame([])
    df.to_excel(excel_file, index=False, header=False)
    path = 'gdgx.xlsx'
    data = pd.read_excel(path, sheet_name='Table1')
    modu = Tianyancha()  # 创建天眼查查询类
    flag = True
    for company in data.values:
        try:
            if flag:
                modu.quit_driver()
                modu.int_driver()  # 初始化浏览器设置
                modu.int_home()
            flag = False
            if len(company) > 5 and company[4] is not None and isinstance(company[4], str):
                continue
            name = company[1]
            if name == '企业名称':
                continue
            name.replace('*', '')
            base = modu.search(name, company)
            if base is None:
                print('error')
                continue

            name_fix = name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
            search_name_fix = base.name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
            if name_fix == search_name_fix:
                print_info(base, 1)
            else:
                base2 = modu.search(name, company)
                if base == base2:
                    print_info(base, 2)
                else:
                    search_name_fix2 = base2.name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
                    if name_fix == search_name_fix2:
                        print_info(base2, 3)
                    else:
                        base3 = modu.search(name, company)
                        print_info(base3, 4)
        except Exception as e:
            print('error')
            print(e)
            flag = True
    modu.quit_driver()  # 关闭浏览
    print(1)
