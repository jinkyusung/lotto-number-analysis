import lotto
import pandas as pd
import webbrowser
from pretty_html_table import build_table
import random

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


if __name__ == '__main__':
    url = "https://dhlottery.co.kr/common.do?method=main"
    lotto_dates, lotto_nums = lotto.get_every_lotto(url)

    df = lotto_onehot(lotto_dates, lotto_nums)
    result = mean_var_df(df)

    print(result)

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
