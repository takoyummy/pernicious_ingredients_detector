from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject

path = "/Users/ansea/Desktop/sparta/test_ocr/chromedriver_mac64/chromedriver"
driver = webdriver.Chrome(path)
driver.get("http://www.chemistory.go.kr/kor/material/db.do?menuNo=12002")

for page in range(1, 25):
    driver.execute_script("linkPage(" + str(page) + ");")
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    time.sleep(2)
    common_datas = soup.select('#contents > div.chemiBox > ul > li')
    for common_data in common_datas:

        a_tag = common_data.select_one('div.chemiTopBox > h3')
        b_tag = common_data.select_one('div.chemiTopBox > div')

        if a_tag is not None:
            name = a_tag.find(text=True, recursive=False).strip()
            desc = b_tag.find(text=True, recursive=False).strip()

            print(name)
            print(desc)
            # # mongoDB에 저장하는 부분(insert 중복 실행을 방지하기 위해 주석 처리)
            # info = {
            #     'name': name,
            #     'desc': desc,
            #
            # }
            # db.project.insert_one(info)
