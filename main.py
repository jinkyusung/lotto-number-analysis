import lotto
import datetime
import pandas as pd


def onehot(data: list[list]) -> list:
    def encode(nums: list):
        dummy = [0] * 45
        for n in nums:
            dummy[n - 1] = 1
        return dummy
    return list(map(encode, data))


def lotto_df(index: list, data: list[list]):
    df = pd.DataFrame(data=onehot(data), index=index, columns=list(range(1, 46)))
    return df


def mean_var_df(lotto_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df['Mean'] = lotto_df.mean()
    df['Variance'] = lotto_df.var()
    return df.T


if __name__ == '__main__':
    url = "https://dhlottery.co.kr/common.do?method=main"
    while 1:
        my_choice = input("<select>\n1. until yy-mm-dd\n2. until now \nselect : ")
        if my_choice == '1':
            my_year = input()
            if lotto.check_input_year(my_year):
                #print(type(my_year))   #string
                #print(my_year)
                break
        elif my_choice == '2':
            today_date = str(datetime.datetime.today())
            my_year = today_date[2:10]
            #print(my_year)
            break
        else:
            print('choose 1 or 2\n')


    lotto_dates, lotto_nums = lotto.get_every_lotto(url, my_year)
    result1 = lotto_df(lotto_dates, lotto_nums)
    result2 = mean_var_df(result1)

    print(result1)
    print(result2)
