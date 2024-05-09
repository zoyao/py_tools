import random
import time

from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker
import base64
from captcha import Captcha


fake = Faker("zh_CN")
captcha = Captcha(is_sleep=False)


def run(playwright: Playwright) -> None:
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )
        page = context.new_page()

        page.goto("https://www.shtjtv.com/web/#/pages/public/webH5?href=%22https%3A%2F%2Fwork.jingjia-tech.com%2Fhtsec%2Fqs%2F%23%2F1770648471997648896%22")
        page.frame_locator("iframe").get_by_role("button", name="立即注册").click()
        # page.frame_locator("iframe").get_by_placeholder("请输入姓名").click()
        page.frame_locator("iframe").get_by_placeholder("请输入姓名").fill(fake.name())
        # page.frame_locator("iframe").get_by_placeholder("请输入手机号").click()
        page.frame_locator("iframe").get_by_placeholder("请输入手机号").fill(fake.phone_number())
        # page.frame_locator("iframe").locator("form div").filter(has_text="学校 *请输入学校名称").get_by_role("textbox").click()
        page.frame_locator("iframe").locator("form div").filter(has_text="学校 *请输入学校名称").get_by_role("textbox").fill("广东科贸")
        page.frame_locator("iframe").get_by_text("广东科贸职业学院").first.click()
        page.frame_locator("iframe").get_by_role("button", name="注册，并开始答题").click()

        image_search_str = page.frame_locator("iframe").locator(".captcha-tip img").first.get_attribute('src')
        image_str = page.frame_locator("iframe").locator(".captcha-img img").first.get_attribute('src')
        image_search_str = image_search_str[image_search_str.index(',') + 1:]
        image_str = image_str[image_str.index(',') + 1:]
        image_search = base64.b64decode(image_search_str)
        image = base64.b64decode(image_str)
        trackList = captcha.search_track_list(image_search, image)

        address = page.frame_locator("iframe").locator(".captcha-img img").first.bounding_box()

        for track in trackList:
            page.mouse.move(address['x'] + (track['x'] * 180 / 360) + random.randint(-100, 100),
                            address['y'] + (track['y'] * 300 / 590) + random.randint(-200, 200))
            time.sleep(random.randint(1, 2))
            page.mouse.move(address['x'] + (track['x'] * 180 / 360),
                            address['y'] + (track['y'] * 300 / 590))
            page.mouse.click(address['x'] + (track['x'] * 180 / 360) + random.randint(-10, 10),
                             address['y'] + (track['y'] * 300 / 590) + random.randint(-10, 10))
            time.sleep(random.randint(1, 5))
    except Exception:
        pass
    finally:
        if page:
            try:
                page.close()
            except Exception:
                pass
        if context:
            try:
                context.close()
            except Exception:
                pass
        if browser:
            browser.close()


with sync_playwright() as playwright:
    for i in range(20):
        try:
            run(playwright)
        except Exception:
            pass
        time.sleep(random.randint(20, 100))
