def check(c, detail):
    flag = False
    words = '【无】'
    if 'keywords' in c.keys():
        for keys in c['keywords']:
            # keywords 内任意满足即可
            words = ''
            key_flag = True
            for key in keys.split(','):
                # 以','分割内容需全部满足
                words += '【' + key + '】'
                if key not in detail:
                    # 匹配失败
                    key_flag = False
                    break
            if key_flag:
                # 匹配成功
                flag = True
                break
    else:
        # keywords 无数据，全部推送
        flag = True
    return flag, words