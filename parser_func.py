import time

import requests
import user_config
from bs4 import BeautifulSoup
from selenium import webdriver
import hashing
import os
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display



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



def parse(driver, delay):

    while True:
        split_symbol = "  #  "

        href_arr = []
        info_arr = []

        while True:
            time.sleep(7)

            soup = BeautifulSoup(driver.page_source, features="html.parser")

            adds = driver.find_elements_by_class_name("close")
            for elem in adds:
                try:
                    elem.click()
                except:
                    pass

            hrefs = soup.find_all("td", {"class": "align-middle pr-0 text-right"})
            info = soup.find_all("td", {"class": "px-0"})

            href_arr += (list(map(lambda x: (f'https:{x.find_all("a")[0].get("href")}'), hrefs)))
            info_arr += (list(map(lambda x: (x.findAll(text=True))[:3], info)))


            try:
                next = driver.find_elements_by_css_selector(".btn.btn-link.text-decoration-none")
                next[len(next) - 1].click()
            except:

                driver.find_element_by_xpath('//*[@id="kvk-header"]/div/a').click()


                # Test (close traceback add)
                try:
                    driver.find_element_by_class_name("ns-vnrx1-e-16").click()
                except:
                    pass


                # print("Finished\n\n************************************")
                # print(href_arr)
                # print("\n\n************************************")
                # print(info_arr)
                break


        parse_list = []
        temp_href_arr = []
        for i in range(0, len(info_arr)):
            info_arr[i][0] = info_arr[i][0].strip()
            info_arr[i][1] = info_arr[i][1].strip()

            if (info_arr[i][:2] != ['Без названия', 'Неизвестен']):
                parse_list.append(info_arr[i][:2])
                temp_href_arr.append(href_arr[i])
        href_arr = temp_href_arr


        file_list = os.listdir(str(os.getcwd()) + "\Music_Output")
        file_list = list(map(lambda x: x.split(".")[0].split(split_symbol), file_list))

        if hash_check(parse_list, file_list) == False:
            print("Loading files...")

            index = 0
            for item in parse_list:
                if item not in file_list:
                    r = requests.get(href_arr[index], allow_redirects=True)
                    open(f'Music_Output\{str(item[0]) + split_symbol + str(item[1])}.mp3', 'wb').write(r.content)
                index += 1

            for item in file_list:
                if item not in parse_list:
                    os.remove(f'Music_Output\{str(item[0]) + split_symbol + str(item[1])}.mp3')
        time.sleep(60 * delay)






def hash_check(info_arr_1, info_arr_2):
    if hashing.hash(info_arr_1) == hashing.hash(info_arr_2):
        return True
    else:
        return False