from playwright.sync_api import Playwright, sync_playwright

# from boss import run

info = '证券'
job_name_search = ['后台', '柜台', '柜员', '综合', '合规', '开户', '人事']
job_name_ignore = ['实习', '经纪', '投顾', '顾问', '客户', '总经理', '负责人', '总监', '理财', '工程', '讲师', '产品', '运营',
                   '运维', '营销', '分析', '证券从业人员', '培训', '渠道', '证券经理', '业务经理', '项目经理', '投资咨询', '研究',
                   '模型', '拓展', '财富规划', '财富经理', '财富管理', '财富机构', '纪纪', '零售经理', '电销', '机构业务', '承揽',
                   '管培生']
company = ['证券']
company_ignore = ['咨询']

# with sync_playwright() as playwright:
#     try:
#         run(playwright, info, job_name_search, job_name_ignore, company)
#     except Exception as e:
#         print(e)