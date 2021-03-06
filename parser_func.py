
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
import logging
import zipfile
import requests
import config
import hashing
# import pwinput


'''
This function creates .zip archive
consisting of all Music_Output/ directory
files. It is implemented by use of basic
zipfile library.  
'''
def compress_zip():
    z = zipfile.ZipFile('Music.zip', 'w')
    file_list = os.listdir(str(os.getcwd()) + "/Music_Output")

    for file in tqdm(file_list):
        z.write(f'Music_Output/{file}')
    z.close()

    return os.path.getsize('Music.zip')


'''
This function search and returns
the id of google drive default "Music" folder.
In case there is no such folder, it would be
created automatically in root directory. 
'''
def get_drive_folder_id(google_drive):
    folder_id = ''
    for i in range(0, 2):
        for file in google_drive.files().list().execute()['files']:
            if file['name'] == 'Music':
                folder_id = (file["id"])
                return folder_id

        if not folder_id:
            folder_metadata = {'name': 'Music', 'mimeType': 'application/vnd.google-apps.folder'}
            google_drive.files().create(body=folder_metadata).execute()
            logging.info(f'Created new Google Drive "Music" folder')
        else:
            return folder_id


'''
This function simply returns
the list of all existing files
in default google drive "Music" folder.
'''
def get_drive_file_list(google_driver):
    results = google_driver.files().list(q="'" + get_drive_folder_id(google_driver) + "' in parents", fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


'''
This function uploads Music.zip file
to Music/ directory of your google drive.
Also, it uses size check to compare local 
zip file with google drive zip file.
'''
def upload_zip(google_drive):
    # Check zip file size
    zip_size = 0
    zip_id = ''
    for item in get_drive_file_list(google_drive):
        if item['name'] == 'Music.zip':
            zip_id = item['id']
            zip_size = (google_drive.files().get(fileId=zip_id, fields='size').execute())['size']
            break

    # Upload zip archive if it's different or did not exist
    if zip_size != compress_zip():
        try:
            google_drive.files().delete(fileId=zip_id).execute()
        except:
            pass

        zip_metadata = {'name': f'Music.zip', 'parents': [get_drive_folder_id(google_drive)]}
        media = MediaFileUpload(f'Music.zip', mimetype='application/zip', resumable=True)
        google_drive.files().create(body=zip_metadata, media_body=media, fields='id').execute()


'''
This function returns current list 
of files in the Music_Output/ local
directory and splits it by author and
song name. 
'''
def get_file_list(split_symbol):
    file_list = os.listdir(str(os.getcwd()) + "/Music_Output")
    file_list = list(map(lambda x: x.split(".mp3")[0].split(split_symbol), file_list))
    return file_list


'''
This function simply compare 
two arrays by invoking hash function
in hashing.py.
'''
def hash_check(info_arr_1, info_arr_2):
    if hashing.hash(info_arr_1) == hashing.hash(info_arr_2):
        return True
    else:
        return False


'''
This function automatically log-in
to kiss-vk, using your VK profile authorization
(message or telephone call verification).
You could enter your login and password data
by simple console input (safe_auth = False) or by modifying
config.py (safe_auth = True).
'''
def login(driver, safe_auth = True):
    login_url = 'https://oauth.vk.com/authorize?client_id=6757658&display=page&redirect_uri=https%3A%2F%2Flogin-kissvk.info%2Fkvk%2Fkvk-auth-redirecter.html%3Fkvk_auth_url_prefix%3Dhttps%253A%252F%252Fkissvk.com%252F&scope=offline&response_type=token&v=5.110&state=123456&revoke=1'
    driver.get(login_url)

    if safe_auth:
        login_elem = driver.find_element_by_name("email")
        pass_elem = driver.find_element_by_name("pass")
    else:
        config.User.login = input("Enter user login:")
        config.User.password = input("Enter user password:")
        # config.User.login = pwinput.pwinput(prompt="Enter user login:")
        # config.User.password = pwinput.pwinput(prompt="Enter user password:")

    login_elem.send_keys(config.User.login)
    pass_elem.send_keys(config.User.password)
    driver.find_element_by_id("install_allow").click()

    time.sleep(10)
    code_elem = driver.find_element_by_name("code")
    config.User.ver_code = input("Enter verification code:")
    code_elem.send_keys(str(config.User.ver_code))
    driver.find_element_by_class_name("button").click()
    time.sleep(20)
    logging.info(f'Bot has been successfully logged in as: {config.User.login}  ver. key: {str(config.User.ver_code)}')


'''
This is the main function to parse, download
and upload all the content.

** ITER_DELAY=<int> - regulates delay between
  every iteration (in minutes, default = 0). 
  It did not affect on overall code performance (speed).
  
** OVERALL_DELAY=<int> - regulates inner code
  delay (works as multiplier default = 1). 
  IT AFFECTS ON OVERALL CODE PERFORMANCE!
  increase it in case you have slow 
  internet connection or low performance PC.  
'''
daily_uploaded = False
def parse(driver, google_drive, iter_delay=0, overall_delay=1, split_symbol = "  #  "):

    global daily_uploaded

    href_arr = []
    info_arr = []

    try:
        driver.find_element_by_xpath('//*[@id="kvk-header"]/div/a').click()
    except:
        pass

    while True:
        time.sleep(4 * overall_delay)

        try:
            try:
                while True:
                    driver.find_element_by_xpath('/html/body/div/div[1]/div/div[3]/span').click()
                    time.sleep(0.5 * overall_delay)
            except:
                pass


            driver.find_element_by_xpath('//*[@id="dismiss-button"]').click()
            time.sleep(5 * overall_delay)
        except:
            pass

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
            test_elem = driver.find_element_by_xpath('//*[@id="kvk-header"]/div/a')
            driver.execute_script("arguments[0].click();", test_elem)
            break


    parse_list = []
    temp_href_arr = []
    illegal_sym = ['<', '>', ':', '"', '/', '|', '\\', '?', '*']

    for i in range(0, len(info_arr)):
        info_arr[i][0] = str(info_arr[i][0].strip()).replace('/', '')
        info_arr[i][1] = info_arr[i][1].strip()

        for sym in illegal_sym:
            if sym in info_arr[i][0]:
                info_arr[i][0] = info_arr[i][0].replace(sym, '')

            if sym in info_arr[i][1]:
                info_arr[i][1] = info_arr[i][1].replace(sym, '')

        if (info_arr[i][:2] != ['?????? ????????????????', '????????????????????']):
            parse_list.append(info_arr[i][:2])
            temp_href_arr.append(href_arr[i])
    href_arr = temp_href_arr


    # Reduce collisions by renaming
    for i in parse_list:
        counter = 0
        i = [i[0].upper(), i[1].upper()]
        index = 0
        name_index = 1
        for j in parse_list:
            j = [j[0].upper(), j[1].upper()]
            if i == j:
                if counter != 0:
                    parse_list[index][1] += f" ({name_index})"
                    name_index += 1
                counter += 1
            index += 1



    file_list = get_file_list(split_symbol)

    if hash_check(parse_list, file_list) == False:
        driver.save_screenshot("last_screenshot.png")
        print("Loading files...")
        removed_files = []
        added_files = []
        warning_files = []
        index = 0
        for item in parse_list:
            if item not in file_list:
                file_name = str(item[0]) + split_symbol + str(item[1])
                r = requests.get(href_arr[index], allow_redirects=True)
                open(f'Music_Output/{file_name}.mp3', 'wb').write(r.content)
                added_files.append(f'{str(item[0]) + split_symbol + str(item[1])}.mp3')
            index += 1

        for item in file_list:
            file_name = str(item[0]) + split_symbol + str(item[1])

            if item not in parse_list:
                os.remove(f'Music_Output/{file_name}.mp3')
                removed_files.append(f'{file_name}.mp3')
            elif os.path.getsize(f'Music_Output/{file_name}.mp3') == 0:
                warning_files.append(f'{file_name}.mp3')

        if warning_files:
            logging.warning(f'Some files have ZERO SIZE (please download and replace them manually): {str(warning_files)}')
        if added_files:
            logging.info(f'Some files have been ADDED: {str(added_files)}')
        if removed_files:
            logging.info(f'Some files have been REMOVED: {str(removed_files)}')

    print("Finished!")



    cur_time_H = int(datetime.now().strftime("%H"))

    time_from = int(config.Settings.upload_time.split(' - ')[0].split(':')[0])
    time_till = int(config.Settings.upload_time.split(' - ')[1].split(':')[0])

#   Reset daily upload flag in 00:00
    if 0 <= cur_time_H <= (iter_delay / 60) * 2:
        daily_uploaded = False

#   Upload only at night
    if (time_from <= cur_time_H <= time_till) and daily_uploaded == False:
        upload_zip(google_drive)
        daily_uploaded = True


    time.sleep(60 * iter_delay)