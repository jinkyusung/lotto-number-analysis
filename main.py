import pandas as pd
import webbrowser
from pretty_html_table import build_table
import random
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By


def compare_date(date1, date2):
    try:
        datetime.datetime.strptime(date1, "%y-%m-%d")
        datetime.datetime.strptime(date2, "%y-%m-%d")
        year1 = date1[:2]
        year2 = date2[:2]
        if year1 > year2:
            return 0
        elif year2 > year1:
            return 1
        else :
            month1 = date1[3:5]
            month2 = date2[3:5]
            if month1 > month2:
                return 0
            elif month1 < month2:
                return  1
            else:
                if date1[-2:] >= date2[-2:]:
                    return 0
                elif date1[-2:] < date2[-2:]:
                    return 1
    except ValueError:
        print("Incorrect data format({0}), should be YY-MM-DD".format(my_year))
        return False


def get_number(driver, url):   #마지막 번호가 보너스 번호

    lotto_year = driver.find_element(By.ID, 'drwNoDate').text
    if lotto_year[0] == '[':
        lotto_year = lotto_year[3:-1]
    else:
        lotto_year = lotto_year[2:]
    if INPUT_YEAR_MODE:
        if compare_date(my_year, lotto_year):  #my_year 가 더 작으면 작동하지 않는다
            return 0, 0

    result_number=[]
    for i in range(1, 7):
        text_number = driver.find_element(By.ID, 'drwtNo'+str(i)).text
        result_number.append(int(text_number))
    text_bonus_number = driver.find_element(By.ID, 'bnusNo').text
    result_number.append(int(text_bonus_number))


    return lotto_year, result_number


def get_every_lotto(url):   #모든 로또회차 구하기 (연도 리스트, 번호 리스트)
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    tabs = driver.window_handles

    for handle in tabs: #팝업 닫기
        if handle != tabs[0]:
            driver.switch_to.window(handle)
            driver.close()
    driver.switch_to.window(tabs[0])    #메인 홈페이지 창으로 선택

    prev_button = driver.find_element(By.CLASS_NAME, 'go.prev') #이전회 버튼

    text_times = driver.find_element(By.ID, 'lottoDrwNo').text
    times = int(text_times) #전체 회차, 1000회가 넘어서 오래걸릴까봐 일단 구해놓기만 함

    years = []
    lotto_nums = []

    for i in range(times): #여기에 원하는 횟수만큼 대입해서 값 가져오기
        temp_year, temp_lotto_num = get_number(driver, url)
        if temp_year == 0 or temp_lotto_num == 0:   #원하는 연도보다 이후 것
            prev_button.click()
            continue
        years.append(temp_year)
        lotto_nums.append(temp_lotto_num)
        prev_button.click()
    return years, lotto_nums


def check_input_year(my_year):
    try:
        datetime.datetime.strptime(my_year, "%y-%m-%d")
        return True
    except ValueError:
        print("Incorrect data format({0}), should be YY-MM-DD".format(my_year))
        return False


def onehot(data: list[list]) -> list:
    def encode(nums: list):
        dummy = [0] * 45
        for n in nums:
            dummy[n - 1] = 1
        return dummy
    return list(map(encode, data))


def lotto_onehot(index: list, data: list[list]):
    df = pd.DataFrame(data=onehot(data), index=index, columns=list(range(1, 46)))
    return df


def mean_var_df(lotto_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df['Mean'] = round(lotto_df.mean(), 3)
    df['Variance'] = round(lotto_df.var(), 3)
    return df.T


def table_to_html(df):
    colors = ['blue', 'yellow', 'grey', 'blue', 'orange', 'red', 'green']
    themes = ['light', 'dark']

    html = """<html lang="ko">
          <head>
          <meta charset="utf-8">
            <style type="text/css">
                p {
                    font-family:'consolas'
                }
            </style>
            <title>Lotto Mean and Variance</title>
          </head>
          <body>
            <h1>Mean and Variance of Lotto numbers</h1>
            <a>Dataframe be printed by using <p/>pretty_html_table</p> </a>
          </body>
        </html>"""

    random_theme = colors[random.randint(0, 6)] + '_' + themes[random.randint(0, 1)]
    table = build_table(result, random_theme, width='auto', index=True)
    html += table

    filepath = "result.html"
    with open(filepath, 'w') as f:
        f.write(html)
    f.close()
    webbrowser.open_new_tab(filepath)


if __name__ == '__main__':

    url = "https://dhlottery.co.kr/common.do?method=main"
    while 1:
        my_choice = input("<select>\n1. until yy-mm-dd\n2. until now \nselect : ")
        if my_choice == '1':
            my_year = input()
            if check_input_year(my_year):
                # print(type(my_year))   #string
                # print(my_year)
                break
        elif my_choice == '2':
            today_date = str(datetime.datetime.today())
            my_year = today_date[2:10]
            # print(my_year)
            break
        else:
            print('choose 1 or 2\n')


    INPUT_YEAR_MODE = 1  # 입력한 날짜까지만 나오도록
    lotto_dates, lotto_nums = get_every_lotto(url)

    df = lotto_onehot(lotto_dates, lotto_nums)
    result = mean_var_df(df)

    print(result)

    table_to_html(result)