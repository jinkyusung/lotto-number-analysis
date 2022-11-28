import lotto
import pandas as pd
import os


def onehot(data: list[list]):
    def encode(nums: list):
        dummy = [0] * 45
        for n in nums:
            dummy[n - 1] = 1
        return dummy
    return list(map(encode, data))


def make_dataframe(index, data):
    df = pd.DataFrame(data=onehot(data), index=index, columns=list(range(1, 46)))
    return df


if __name__ == '__main__':
    url = "https://dhlottery.co.kr/common.do?method=main"
    lotto_dates, lotto_nums = lotto.get_every_lotto(url)
    lotto_df = make_dataframe(lotto_dates, lotto_nums)
    path = os.getcwd().replace('\\','/') + '/lotto_df.csv'
    lotto_df.to_csv(path)
