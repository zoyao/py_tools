import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.shtjtv.com/web/#/pages/public/webH5?href=%22https%3A%2F%2Fwork.jingjia-tech.com%2Fhtsec%2Fqs%2F%23%2F1770648471997648896%22")
    page.frame_locator("iframe").get_by_role("button", name="立即注册").click()
    page.frame_locator("iframe").get_by_placeholder("请输入姓名").click()
    page.frame_locator("iframe").get_by_placeholder("请输入姓名").fill("林是")
    page.frame_locator("iframe").get_by_placeholder("请输入手机号").click()
    page.frame_locator("iframe").get_by_placeholder("请输入手机号").fill("13209806785")
    page.frame_locator("iframe").locator("form div").filter(has_text="学校 *请输入学校名称").get_by_role("textbox").click()
    page.frame_locator("iframe").locator("form div").filter(has_text="学校 *请输入学校名称").get_by_role("textbox").fill("珠海kyi")
    page.frame_locator("iframe").locator(".n-popover").click()
    page.frame_locator("iframe").get_by_text("北京师范大学珠海分校").first.click()
    page.frame_locator("iframe").get_by_role("button", name="注册，并开始答题").click()
    page.frame_locator("iframe").locator(".captcha-bg-mask").click(button="right")
    page.frame_locator("iframe").locator(".captcha-bg-mask").click()
    page.frame_locator("iframe").locator("div").filter(has_text=re.compile(r"^1$")).nth(1).click()
    page.frame_locator("iframe").get_by_text("12").click()
    page.frame_locator("iframe").locator("div").filter(has_text=re.compile(r"^请依次点击：$")).locator("img").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
