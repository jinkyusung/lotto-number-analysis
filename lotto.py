from selenium import webdriver
from selenium.webdriver.common.by import By

def get_number(driver, url):   #마지막 번호가 보너스 번호

    result_number=[]
    for i in range(1, 7):
        text_number = driver.find_element(By.ID, 'drwtNo'+str(i)).text
        result_number.append(int(text_number))
    text_bonus_number = driver.find_element(By.ID, 'bnusNo').text
    result_number.append(int(text_bonus_number))

    lotto_year = driver.find_element(By.ID, 'drwNoDate').text
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
    for i in range(times):
        temp_year, temp_lotto_num = get_number(driver, url)
        years.append(temp_year)
        lotto_nums.append(temp_lotto_num)
        prev_button.click()
    return years, lotto_nums


if __name__ == '__main__':
    url = "https://dhlottery.co.kr/common.do?method=main"
    print(get_every_lotto(url))
