import random
import time

from playwright.sync_api import Playwright, sync_playwright, expect
from faker import Faker
import base64
from captcha import Captcha


fake = Faker("zh_CN")
captcha = Captcha(is_sleep=False)
success = 0


def run(pw: Playwright, index: str) -> None:
    try:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 600, 'height': 1000}
        )
        page = context.new_page()

        page.goto("https://www.shtjtv.com/web/#/pages/public/webH5?href=%22https%3A%2F%2Fwork.jingjia-tech.com%2Fhtsec%2Fqs%2F%23%2F1770648471997648896%22")

        a = page.locator("iframe").first.get_attribute('src')


        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").get_by_role("button", name="立即注册").click()
        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").get_by_placeholder("请输入姓名").fill(fake.name())
        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").get_by_placeholder("请输入手机号").fill(fake.phone_number())
        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").locator("form div").filter(has_text="学校 *请输入学校名称").get_by_role("textbox").fill("广东科贸")
        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").get_by_text("广东科贸职业学院").first.click()
        time.sleep(random.randint(1, 3))
        page.frame_locator("iframe").get_by_role("button", name="注册，并开始答题").click()
        time.sleep(random.randint(1, 3))

        image_search_str = page.frame_locator("iframe").locator(".captcha-tip img").first.get_attribute('src')
        image_str = page.frame_locator("iframe").locator(".captcha-img img").first.get_attribute('src')
        image_search_str = image_search_str[image_search_str.index(',') + 1:]
        image_str = image_str[image_str.index(',') + 1:]
        image_search = base64.b64decode(image_search_str)
        image = base64.b64decode(image_str)
        captcha_result = captcha.search(image_search, image)

        address = page.frame_locator("iframe").locator(".captcha-img img").first.bounding_box()
        x_ratio = address['height'] / captcha_result['height']
        y_ratio = address['width'] / captcha_result['width']
        for track in captcha_result['track_list']:
            x_fix = address['x'] + (track['x'] * x_ratio)
            y_fix = address['y'] + (track['y'] * y_ratio)
            page.mouse.move(x_fix + random.randint(-100, 100), y_fix + random.randint(-200, 200))
            time.sleep(random.randint(1, 2))
            page.mouse.move(x_fix, y_fix)
            page.mouse.click(x_fix + random.randint(-5, 5), y_fix + random.randint(-5, 5))
            time.sleep(random.randint(1, 5))

        iframe_src = page.locator("iframe").first.get_attribute('src')
        if '?step=' not in iframe_src:
            global success
            success += 1
        page.screenshot(path="./results/result_" + index + ".png")
    except Exception as e:
        print(e)
    finally:
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
    for i in range(20):
        if i > 0:
            time.sleep(random.randint(20, 100))
        try:
            run(playwright, index + str(i))
        except Exception as e:
            print(e)
        print(index + "\ttotal:" + str(i) + "\tsuccess:" + str(success) + "")
