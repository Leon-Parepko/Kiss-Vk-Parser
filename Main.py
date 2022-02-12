import hashing
import parser_func
from selenium import webdriver
from pyvirtualdisplay import Display

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
    parser_func.parse(driver, 20)




    # except Exception as e:
    #     print(e)
    # pass

    if driver:
        driver.close()

    # if display:
    #   display.stop()

