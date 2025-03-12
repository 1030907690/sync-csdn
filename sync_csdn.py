from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.webdriver import WebDriver
import time


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


def article_list(driver: WebDriver):
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

        print(a_href + " " + p2.text.split(" ")[0] + " " + a_text)
        # print(a_tag.text)


def next_page(driver: WebDriver):
    driver.implicitly_wait(15)
    next_btn = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div/div/div/div[2]/section/div/div[1]/div/section/section/main/div/div/div/div/div/div/div[4]/div/button[2]")
    btn_disabled = next_btn.get_attribute("disabled")
    print("btn_disabled " ,btn_disabled)
    if next_btn is not None and btn_disabled is None:
        next_btn.click()
        return True
    return False


if __name__ == '__main__':
    driver = create_driver()
    start_page(driver)
    click_visible(driver)
    article_list(driver)
    while next_page(driver):
        article_list(driver)

    input("按任意键结束")
    # assert "Python" in driver.title
    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()
