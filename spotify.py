from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import json
from time import sleep
from bs4 import BeautifulSoup
import sys
import os

gui_options = Options()
gui_options.add_argument('--log-level=3')

def question():
    qSilence = input("Тихий перенос (без отображения GUI) Y/N ?\n")
    if qSilence == "Y":
        gui_options.headless = True
        os.system('cls')
    elif qSilence == "N":
        gui_options.headless = False
        os.system('cls')
    else:
        os.system('cls')
        print("Введите Y или N")
        question()

question()

driver = webdriver.Chrome(options=gui_options)
wait = WebDriverWait(driver, 30)
wait_for_track = WebDriverWait(driver, 3)

def login_vk():
    try:
        vk_login = json.load(open("data.json"))['vk']['login']
        vk_pass = json.load(open("data.json"))['vk']['password']
        driver.get("https://vk.com/login")
        wait.until(ec.visibility_of_element_located((By.ID, 'email')))
        login_field_vk = driver.find_element_by_id("email").send_keys(vk_login)
        wait.until(ec.visibility_of_element_located((By.ID, 'pass')))
        pass_field_vk = driver.find_element_by_id("pass").send_keys(vk_pass)
        wait.until(ec.visibility_of_element_located((By.ID, 'login_button')))
        submit_vk = driver.find_element_by_id("login_button").click()
        return print("Вход в VK успешен")
    except:
        return False

def Go_to_music_vk():
    try:
        wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="l_aud"]/a')))
        music_vk = driver.find_element_by_xpath('//*[@id="l_aud"]/a').click()
        print("Перешёл в раздел музыки")
    except:
        return False

def Scroll_page():
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("Страница успешно проскроллена")
        return 
    except:
        return False

def Get_music_list(music_vk_html, music_vk_list):
    try:
        for i in driver.find_elements_by_class_name("audio_row__inner"):
            music_vk_html.append(i.get_attribute("innerHTML"))
        for i in range(len(music_vk_html)):
            soup = BeautifulSoup(music_vk_html[i], "lxml")
            music = soup.find(class_="audio_row__title_inner _audio_row__title_inner").text
            music += " " + soup.find("a").text
            music_vk_list.append(music)
        print(f"Список песен получен\nКоличество песен:{len(music_vk_list)}")
    except:
        return False

def login_spotify():
    try:
        spotify_login = json.load(open("data.json"))['spotify']['login']
        spotify_pass = json.load(open("data.json"))['spotify']['password']
        driver.get("https://accounts.spotify.com/ru/login/?continue=https://open.spotify.com/search")
        wait.until(ec.visibility_of_element_located((By.ID, 'login-username')))
        login_field_spotify = driver.find_element_by_id("login-username").send_keys(spotify_login)
        wait.until(ec.visibility_of_element_located((By.ID, 'login-password')))
        pass_field_spotify = driver.find_element_by_id("login-password").send_keys(spotify_pass)
        wait.until(ec.visibility_of_element_located((By.ID, 'login-button')))
        submit_spotify = driver.find_element_by_id("login-button").click()
        print("Вход в Spotify успешен")
    except:
        return False

def Translate_BMP(list_obj):
    new_list = []
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    for i in range(len(list_obj)):
        new_list.append(list_obj[i].translate(non_bmp_map))
    return new_list

def Add_music(music_vk_list):
    translated_list = Translate_BMP(music_vk_list)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/input')))
    translated_list.reverse()
    for i in range(len(translated_list)):
        try:
            print("============================")
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/input').send_keys(translated_list[i]) #search field
            wait_for_track.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="searchPage"]/div/div/section[2]/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/button'))) # wait for button
            driver.find_element_by_xpath('//*[@id="searchPage"]/div/div/section[2]/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/button').click() #heart click
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/div/button').click() #clean searh
            print(f"Трек '{translated_list[i]}' успешно добавлен\nОсталось треков:{len(translated_list) - i}")
            wait_for_track.until(ec.url_changes(driver.current_url))
        except:
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/div/button').click()
            print(f"Не удалось добавить трек {translated_list[i]}\nОсталось треков:{len(translated_list) - i}")
            continue
    
def main():
    music_vk_html = []
    music_vk_list = []

    print("============================")

    if login_vk() == False:
        print("Ошибка при логине в VK")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit()

    print("============================")

    if Go_to_music_vk() == False:
        print("Ошибка при переходе в раздел музыки")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit()

    print("============================")

    if Scroll_page() == False:
        print("Ошибка при скролле страницы")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit()

    print("============================")

    if Get_music_list(music_vk_html, music_vk_list) == False:
        print("Ошибка при получении композиций")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit()
    
    print("============================")
    
    if login_spotify() == False:
        print("Ошибка при логине в Spotify")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit()

    print("============================")
    
    if Add_music(music_vk_list) == False:
        print("Ошибка при добавлении музыки в Spotify")
        print("Программа завершиться через 10 секунд")
        print("============================")
        sleep(10)
        sys.exit() 
    
    print("============================")


if __name__ == "__main__":
    main()