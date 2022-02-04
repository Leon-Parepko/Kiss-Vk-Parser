import time

import requests
import user_config
from bs4 import BeautifulSoup
from selenium import webdriver
import hashing
import os
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display



# file_list = os.listdir(str(os.getcwd()) + "\Music_Output")
# file_list = list(map(lambda x: x.split(".")[0].split("_"), file_list))
print(hashing.hash([["slovo", "qweqwgbhkfdnlkkrdf02fm90"], ["qweqw", "qweqwgbhkfnle3kkdf02fm90"], ["qwaswdasd32r2fqw", "qwdfbdfbdfbm90"], ["qwfnhngfbfdeqw", "2fm9778680"], ["qweqw", "qw"], ["qweqweqwefdsgfdgqw", "qqwef02fm90"], ["qweqw", "qqqwxekdf02fm90"], ["qqweqw", "qweqwgbhkfdnlkkrdf02fm90"], ["qweqw", "qweqwgbhkfnle3kkdf02fm90"], ["qwaswdasd32r2fqw", "qwdfbdfbdfbm90"], ["qwfnhngfbfdeqw", "2fm9778680"], ["qweqw", "qw"], ["qweqweqwefdsgfdgqw", "qqwef02fm90"], ["qweqw", "qqqwxekdf02fm90"], ["qqweqw", "qweqwgbhkfdnlkkrdf02fm90"], ["qweqw", "qweqwgbhkfnle3kkdf02fm90"], ["qwaswdasd32r2fqw", "qwdfbdfbdfbm90"], ["qwfnhngfbfdeqw", "2fm9778680"], ["qweqw", "qw"], ["qweqweqwefdsgfdgqw", "qqwef02fm90"], ["qweqw", "qqqwxekdf02fm90"], ["qqweqw", "qweqwgbhkfdnlkkrdf02fm90"], ["qweqw", "qweqwgbhkfnle3kkdf02fm90"], ["qwaswdasd32r2fqw", "qwdfbdfbdfbm90"], ["qwfnhngfbfdeqw", "2fm9778680"], ["qweqw", "qw"], ["qweqweqwefdsgfdgqw", "qqwef02fm90"], ["qweqw", "qqqwxekdf02fm90"], ["qqweqw", "qweqwgbhkfdnlkkrdf02fm90"], ["qweqw", "qweqwgbhkfnle3kkdf02fm90"], ["qwaswdasd32r2fqw", "qwdfbdfbdfbm90"], ["qwfnhngfbfdeqw", "2fm9778680"], ["qweqw", "qw"], ["qweqweqwefdsgfdgqw", "qqwef02fm90"], ["qweqw", "qqqwxekdf02fm90"]]))
# print(file_list)

# display = Display(visible=0, size=(1, 1))
# display.start()



def login(driver):
    login_url = 'https://oauth.vk.com/authorize?client_id=6757658&display=page&redirect_uri=https%3A%2F%2Flogin-kissvk.info%2Fkvk%2Fkvk-auth-redirecter.html%3Fkvk_auth_url_prefix%3Dhttps%253A%252F%252Fkissvk.com%252F&scope=offline&response_type=token&v=5.110&state=123456&revoke=1'
    driver.get(login_url)
    user_config.User.login = input("Enter user login:")
    user_config.User.password = input("Enter user password:")

    login_elem = driver.find_element_by_name("email")
    pass_elem = driver.find_element_by_name("pass")

    login_elem.send_keys(user_config.User.login)
    pass_elem.send_keys(user_config.User.password)
    driver.find_element_by_id("install_allow").click()

    time.sleep(10)
    code_elem = driver.find_element_by_name("code")
    code_elem.send_keys(input("Enter verification code:"))
    driver.find_element_by_class_name("button").click()



def parse(driver):

    split_symbol = "  #  "

    href_arr = []
    info_arr = []

    while True:
        time.sleep(30)

        soup = BeautifulSoup(driver.page_source, features="html.parser")

        hrefs = soup.find_all("td", {"class": "align-middle pr-0 text-right"})
        info = soup.find_all("td", {"class": "px-0"})

        href_arr += (list(map(lambda x: (f'https:{x.find_all("a")[0].get("href")}'), hrefs)))
        info_arr += (list(map(lambda x: (x.findAll(text=True))[:3], info)))

        # print(href_arr)
        # print(info_arr)

        next = driver.find_elements_by_css_selector(".btn.btn-link.text-decoration-none")
        next[len(next) - 1].click()
        try:
            print(next[len(next) - 1].getAttribute("disabled"))
            break
        except:
            pass

    parse_list = list(map(lambda x: x[:2], info_arr))

    file_list = os.listdir(str(os.getcwd()) + "\Music_Output")
    file_list = list(map(lambda x: x.split(".")[0].split(split_symbol), file_list))

    if hash_check(parse_list, file_list) == False:

        index = 0
        for item in parse_list:
            if item not in file_list:
                r = requests.get(href_arr[index], allow_redirects=True)
                open(f'{str(item[0]) + split_symbol + str(item[1])}.mp3', 'wb').write(r.content)
            index += 1

        for item in file_list:
            if item not in parse_list:
                os.remove(f'{str(item[0]) + split_symbol + str(item[1])}.mp3')





def hash_check(info_arr_1, info_arr_2):
    if hashing.hash(info_arr_1) == hashing.hash(info_arr_2):
        return True
    else:
        return False



def download_files():
    # r = requests.get("https://i114.kissvk.com/api/song/download/get/11/King%20Gnu-Sakayume-kissvk.com.mp3?origin=kissvk.com&url=sid%3A%2F%2F306332812_456239846_5e3dd48a3f140ab34f_d046e9f1b38486eb97&artist=King%20Gnu&title=Sakayume&index=0&user_id=384615283&ui_version=220118202148&future_urls=sid%3A%2F%2F306332812_456239847_64be4b52c51f2a3cfd_6c65bbdf444e082385%2Csid%3A%2F%2F306332812_456239845_e7936891b0f4325470_75582aeb2f4f848517%2Csid%3A%2F%2F306332812_456239843_c5ee4da2467c4b1259_ae334b3217591dcb40%2Csid%3A%2F%2F306332812_456239842_2bc910fac7b065428e_511e822973f4f58c5a%2Csid%3A%2F%2F306332812_456239841_360e42723b94fde72e_9c9a6aa2c8065af1af%2Csid%3A%2F%2F306332812_456239840_25a0abe56e18b21652_3fa52f5b9b83397936%2Csid%3A%2F%2F306332812_456239839_102aef4bb658524cd9_c9b85f969c64b3f958%2Csid%3A%2F%2F306332812_456239838_38728285bbaf002eab_2e2b1531aa02b47685%2Csid%3A%2F%2F306332812_456239837_7ec7a5c732a7b4b4b7_ef677ccdc3b8997507", allow_redirects=True)
    # open('test.mp3', 'wb').write(r.content)
    pass