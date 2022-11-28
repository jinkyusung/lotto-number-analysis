import lotto
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
    lotto_dates, lotto_nums = lotto.get_every_lotto(url)
    result1 = lotto_df(lotto_dates, lotto_nums)
    result2 = mean_var_df(result1)

    print(result1)
    print(result2)
