import time
import re
import numpy as np
import pandas as pd


def insta_searching(word):  #word라는 매개변수를 받는 insta_searching 이라는 함수 생성
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0') 
    #find_element_by_css_selector 함수를 사용해 요소 찾기
    first.click()
    time.sleep(3) #로딩을 위해 3초 대기

def get_content(driver):
    # 1. 현재 페이지의 HTML 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')    
    # 2. 본문 내용 가져오기
    try:  			#여러 태그중 첫번째([0]) 태그를 선택  
        content = soup.select('div.C4VMK > span')[0].text 
        			#첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
                                #태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
    except:
        content = ' ' 
    # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content) # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
    # 4. 작성 일자 가져오기
    try:
        date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10] #앞에서부터 10자리 글자
    except:
        date = ''
    # 5. 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1] 
    except:
        like = 0
    # 6. 위치 정보 가져오기
    try:
        place = soup.select('div.JF9hh')[0].text
    except:
        place = ''
    data = [content, date, like, place, tags]
    return data 

def move_next(driver):
    right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow') 
    right.click()
    time.sleep(3)
    
    

from selenium import webdriver
from bs4 import BeautifulSoup

#1. 크롬으로 인스타그램 - '비정형' 검색
driver = webdriver.Chrome("C:\\Users\\samsung\\Desktop\\chromedriver_win32\\chromedriver.exe")
word = '비정형'
url = insta_searching(word)
driver.get(url) 
time.sleep(4) 
#2. 로그인 하기
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(3) 
elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('ID') 
elem_login = driver.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys('PW') 
time.sleep(1) 
xpath = '//*[@id="loginForm"]/div/div[3]/button/div'
driver.find_element_by_xpath(xpath).click() 
time.sleep(4) 
xpath1 = """//*[@id="react-root"]/section/main/div/div/div/div/button"""
driver.find_element_by_xpath(xpath1).click()
time.sleep(4) 
#3. 검색페이지 접속하기
driver.get(url)
time.sleep(4) 
#4. 첫번째 게시글 열기
select_first(driver) 
#5. 비어있는 변수(results) 만들기
results = [] 
#여러 게시물 크롤링하기
target = 5 #크롤링할 게시물 수
for i in range(target):
    data = get_content(driver) #게시물 정보 가져오기
    results.append(data)
    move_next(driver)    


col = ['contents','date','like','location','hashtag']
df = pd.DataFrame(np.asarray(results),columns=col)

df.to_csv("C:\\Users\\samsung\\Desktop\\연습\\Insta_.csv")

'''
import pandas as pd
raw_total = pd.read_excel("C:\\Users\\samsung\\Desktop\\연습\\Insta_.xlsx")
raw_total.head()
'''
