from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from googletrans import Translator
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import csv

driver = webdriver.Chrome(executable_path="C:/Users/AMS Enterprises/chromedriver.exe")

driver.get("https://a2018010620392131758.szwego.com/static/index.html?t=1601493801996#/goods_list/A2018010620392131758?tagId=13931184")

translator = Translator()

curnt_url = driver.current_url
time.sleep(2)

ans = 0
ans1 = 0
like = driver.find_elements_by_css_selector('.lazy')


ans = len(like)
ans1 = ans

driver.execute_script("window.scrollTo(0, 2500);")
time.sleep(2)
like = driver.find_elements_by_css_selector('.lazy')
ans = len(like)

a1 = 4500

while(ans > ans1):
    ans1 = ans
    driver.execute_script("window.scrollTo(0, " + str(a1) + " );")
    time.sleep(2)

    like = driver.find_elements_by_css_selector('.lazy')

    ans = len(like)
    a1= a1 + 2500
    time.sleep(3)

print("Reached till end")


with open('output-file-name.json', 'w+') as f:


    like = driver.find_elements_by_css_selector('.lazy')
    for x in range(0,len(like)):
        like = driver.find_elements_by_css_selector('.lazy')
        if like[x].is_displayed():
            like[x].click()
            time.sleep(2)

            imgs_link = driver.find_elements_by_css_selector('.w-1-3 img')
            p_Name = driver.find_element_by_css_selector('.ovh .word-break')
            title = str(p_Name.text)

            if '\u2013' in title:

                t1 = title.split('\u2013')[0]
                try:
                    t2 = title.split('\u2013')[1]

                    title = str(t1) + "-" + str(t2)
                except:
                    title = str(t1)
            else:
                pass


            print("Title is ---> " + str(title))

            translation = translator.translate(title, dest='en')
            print(translation.text)    
            title1 = translation.text

            replaces = title1.replace("\n", " ")
            title1 = replaces 

            all_links = []

            for x in range(0,len(imgs_link)):
                imgs_link = driver.find_elements_by_css_selector('.w-1-3 img')
                if imgs_link[x].is_displayed():
                    imgs_link[x].click()
                    time.sleep(3)

                    try:
                        time.sleep(2)
                        img_l = driver.find_element_by_css_selector("#container > div.weui_cells > div:nth-child(3) > div > div > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img")
                        time.sleep(1)
                    except:
                        time.sleep(2)
                        img_l = driver.find_element_by_css_selector("swiper-lazy-loaded")
                        time.sleep(1)

                    print(img_l.get_attribute("src"))
                    links = str(img_l.get_attribute("src"))

                    all_links.append(links)

                    driver.refresh()


            f.write(json.dumps({"Captions":str(title1), "Images":str(all_links)},indent=2).replace("',", "',\n").replace("[" , "[\n").replace("']" , "'\n]"))
            f.write('\n')
            f.write('\n')


        driver.back()
        time.sleep(1)
