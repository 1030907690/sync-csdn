from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # https://blog.csdn.net/weixin_43407092/article/details/97128833 登录保持
    options.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")  # 浏览器路径

    driver = webdriver.Chrome(options=options)
    driver.get("https://mp.csdn.net/mp_blog/manage/article")


    driver.implicitly_wait(15)


    article_divs = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div/div[2]/section/div/div[1]/div/section/section/main/div/div/div/div/div/div/div[3]/div[2]/div[@class='article-list-item-mp']")
    print(article_divs)
    print("---------")
    for article_div in article_divs:
        a_tag = article_div.find_element(By.XPATH,"p[@class='article-list-item-txt']/a")

        print(a_tag.text)


    input("按任意键结束")
    # assert "Python" in driver.title
    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()