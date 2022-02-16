import hashing
import parser_func
from selenium import webdriver
from pyvirtualdisplay import Display
import logging


logging.basicConfig(filename='logging.log', level=logging.INFO, filemode='w', format='%(levelname)s   -   %(asctime)s   -   %(message)s')


if __name__ == '__main__':






    # try:
        # Init Virtual Display (Used on Unix typed OS without GUI)
        # display = Display(visible=0, size=(1, 1))
        # display.start()

        # Init Web Driver
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.maximize_window()

        parser_func.login(driver)

        while True:
            parser_func.parse(driver, 1)




    # except Exception as e:
    #     logging.error(e)
    # pass
    #
    # if driver:
    #     driver.close()

    # if display:
    #   display.stop()







