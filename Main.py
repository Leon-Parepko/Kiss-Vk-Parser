import hashing
import parser_func
from selenium import webdriver
from pyvirtualdisplay import Display
import logging

import user_config
from Google import Create_Service

logging.basicConfig(filename='logging.log', level=logging.INFO, filemode='w', format='%(levelname)s   -   %(asctime)s   -   %(message)s')


if __name__ == '__main__':

    # try:
        # Init Virtual Display (Used on Unix typed OS without GUI)
        # display = Display(visible=0, size=(1, 1))
        # display.start()

        # Init Web Driver
        google_drive = Create_Service(user_config.Drive.secret, user_config.Drive.name, user_config.Drive.version, user_config.Drive.scopes)
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.maximize_window()

        parser_func.login(driver)


        while True:
            parser_func.parse(driver, google_drive, iter_delay=1)



    # except Exception as e:
    #     logging.error(e)
    # pass
    #
    # if driver:
    #     driver.close()
    #
    # if display:
    #   display.stop()







