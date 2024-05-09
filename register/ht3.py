import asyncio
import time

from pyppeteer import launch
from faker import Faker


url = "https://www.shtjtv.com/web/#/pages/public/webH5?href=%22https%3A%2F%2Fwork.jingjia-tech.com%2Fhtsec%2Fqs%2F%23%2F1770648471997648896%22"
# url = "https://work.jingjia-tech.com/htsec/qs/#/1770648471997648896?step=5"
fake = Faker("zh_CN")


async def main():
    browser = await launch(executablePath='C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page = await browser.newPage()
    await page.setViewport({
        "width": 1000,
        "height": 1000
    })

    await page.goto(url)
    await page.querySelectorAll('iframe')
    frame = page.frames[1]
    await frame.waitForSelector('.register-btn')  # 这里可以根据实际情况等待特定的元素或其他条件
    await frame.click('.register-btn')

    inputs = await frame.querySelectorAll('input')
    await inputs[0].focus()
    await page.keyboard.type(fake.name())
    await inputs[1].focus()
    await page.keyboard.type(fake.phone_number())
    await inputs[2].focus()
    await page.keyboard.type("广东科贸职业学院")

    await frame.waitForSelector('.n-base-select-option__content')
    time.sleep(2)
    schools = await frame.querySelectorAll('.n-base-select-option__content')
    await schools[0].hover()
    await page.mouse.down()
    await page.mouse.up()

    await frame.click('.register-btn')
    await page.screenshot({'path': 'example.png'})
    await frame.querySelectorAll('captcha-bg')
    time.sleep(2)


    # 获取页面内容
    content = await page.content()
    print(content)

    # 关闭浏览器
    await browser.close()


# 运行事件循环
asyncio.get_event_loop().run_until_complete(main())
