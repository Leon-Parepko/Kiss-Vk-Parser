


# KISS-VK-PARSER
#  THIS IS A SIMPLE PARSER OF VK MUSIC
#  USING https://kissvk.com/. ALSO, THIS PROGRAM
#  PROVIDES THE ABILITY TO AUTOMATICALLY
#  DOWNLOAD, UPDATE, AND DELETE YOUR MUSIC IN THE LOCAL
#  STORAGE (KIND OF DYNAMIC MUSIC STORAGE).
# CODE BY LPM.
# 2022



'''
Before running this script you should create a
secret token to google drive api application (client_secret.json)
and add one to the root project directory.
Also, you should download and add webdriver
(chromedriver, geckodriver, etc.) to the same root directory.
Make sure you have checked and set up
config.py file.
'''


from selenium import webdriver
from pyvirtualdisplay import Display
from Google import Create_Service
import parser_func
import logging
import os
import config

logging.basicConfig(
                    filename='logging.log',
                    level=logging.INFO,
                    filemode='w',
                    format='%(levelname)s   -   %(asctime)s   -   %(message)s'
                    )


if __name__ == '__main__':
    try:
        google_drive = Create_Service(
                                    config.Drive.secret,
                                    config.Drive.name,
                                    config.Drive.version,
                                    config.Drive.scopes
                                    )

#   Init Virtual Display (Used on Unix typed OS without GUI)
        if config.Settings.os.lower() == "unix":
            display = Display(visible=0, size=(config.Settings.v_screen_res[0], config.Settings.v_screen_res[1]))
            display.start()
            driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver')

        elif config.Settings.os.lower() == "win":
            driver = webdriver.Chrome(executable_path=f'{os.getcwd()}/chromedriver.exe')

        driver.maximize_window()

        parser_func.login(driver)


        while True:
            parser_func.parse(
                            driver,
                            google_drive,
                            iter_delay=config.Settings.iter_delay,
                            overall_delay=config.Settings.overall_delay
                            )



    except Exception as e:
        logging.error(e)

    if driver:
        driver.close()

    if display:
      display.stop()