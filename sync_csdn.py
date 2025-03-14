from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.webdriver import WebDriver
import time
import pydirectinput
import pyperclip

article_list = []


def create_driver():
    options = webdriver.ChromeOptions()
    # https://blog.csdn.net/weixin_43407092/article/details/97128833 登录保持
    options.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")  # 浏览器路径
    driver = webdriver.Chrome(options=options)
    return driver


def start_page(driver):
    driver.get("https://mp.csdn.net/mp_blog/manage/article")
    return driver


def click_visible(driver: WebDriver):
    driver.implicitly_wait(15)
    driver.find_element(By.XPATH,
                        "/html/body/div[2]/div/div/div/div[2]/section/div/div[1]/div/section/section/main/div/div/div/div/div/div/div[1]/div/ul/li[2]/span").click()


def get_article_list(driver: WebDriver):
    time.sleep(3)
    driver.implicitly_wait(15)
    article_divs = driver.find_elements(By.XPATH,
                                        "/html/body/div[2]/div/div/div/div[2]/section/div/div[1]/div/section/section/main/div/div/div/div/div/div/div[3]/div[2]/div[@class='article-list-item-mp']")
    print(article_divs)
    for article_div in article_divs:
        a_tag = article_div.find_element(By.XPATH, "div[@class=\"list-item-mp-right\"]/div/p[1]/a")
        a_href = a_tag.get_attribute("href")
        a_text = a_tag.text
        p2 = article_div.find_element(By.XPATH, "div[@class=\"list-item-mp-right\"]/div/p[2]")
        date = p2.text.split(" ")[0]
        print(a_href + " " + date + " " + a_text)

        article_list.append({"href": a_href, "date": date, "title": a_text})
        # 模拟CTRL + enter键
        # a_tag.send_keys(Keys.CONTROL + Keys.ENTER)
        # print(a_tag.text)


def next_page(driver: WebDriver):
    driver.implicitly_wait(15)
    next_btn = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div/div/div/div[2]/section/div/div[1]/div/section/section/main/div/div/div/div/div/div/div[4]/div/button[2]")
    btn_disabled = next_btn.get_attribute("disabled")
    print("btn_disabled ", btn_disabled)
    if next_btn is not None and btn_disabled is None:
        next_btn.click()
        return True
    return False


def open_new_tag(driver: WebDriver, url: str):
    # 切换标签页
    # driver.switch_to.window(driver.window_handles[0])
    print("打开URL标签页:" + url)
    driver.execute_script('window.open("' + url + '")')
    time.sleep(3)
    print("driver.window_handles ", driver.window_handles)
    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])


def full_selected_copy():
    print("全选")
    pydirectinput.keyDown("ctrl")
    pydirectinput.keyDown("a")
    time.sleep(2)
    pydirectinput.keyUp("a")
    pydirectinput.keyUp("ctrl")

    pydirectinput.keyDown("ctrl")
    pydirectinput.keyDown("c")
    print("复制完成")
    time.sleep(0.01)
    pydirectinput.keyUp("c")
    pydirectinput.keyUp("ctrl")


def click_editor_area(driver: WebDriver, article):
    if article['href'].find("/md/") >= 0:
        editor = driver.find_element(By.XPATH,
                                     "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[@class=\"editor\"]")
        if editor:
            editor.click()

        driver.implicitly_wait(15)
        full_selected_copy()


def copy_to_md(article):
    content = pyperclip.paste()
    with open(article['date'] + "-" + article['title'] + '.md', 'w', encoding='UTF-8') as file:
        file.write(content)


if __name__ == '__main__':
    driver = create_driver()
    start_page(driver)
    click_visible(driver)
    get_article_list(driver)

    # while next_page(driver):
    #     article_list(driver)

    for article in article_list:
        open_new_tag(driver, article['href'])
        click_editor_area(driver, article)
        copy_to_md(article)

    input("按任意键结束")
    driver.close()
