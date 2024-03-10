
import pandas as pd

from bs4 import BeautifulSoup
import requests
import argparse
from pandas import DataFrame

def html_parser_fontanka(year, month, day, name):

    # year = '2024'
    # month = '01'
    # day = '01'
    # name = 'your_name'

    html_text = requests.get(rf'https://www.fontanka.ru/{year}/{month}/{day}/all.html').text

    soup = BeautifulSoup(html_text, 'lxml')

    times = []
    titles = []
    themes = []

    class_li_class = "IBae3" # "HHac3"
    class_time_class = "IBfn" # "HHht"
    class_title_class = "IBd3" # "HHfn"
    class_theme_class = "IBgl IBl7" # "HHjt HHcz"

    for i in soup.find_all('li', class_=class_li_class):
        time = i.find('time', class_=class_time_class)
        title = i.find('a', class_=class_title_class)
        theme = i.find('a', class_=class_theme_class)

        if time is None:
            times.append(None)
        else:
            times.append(time.span.text)

        if title is None:
            titles.append(None)
        else:
            titles.append(title.text)

        if theme is None:
            themes.append(None)
        else:
            themes.append(theme.text)

    # print(times, titles, themes)

    if len(times) == 0:
        print(f"Ничего не было найдено за дату {year}-{month}-{day}")
        print("Либо такой страницы не существуют, либо на сайте были изменены классы элементов")
        return None
    else:
        print(f"Найдено: {len(times)} новостей")

        df = DataFrame({'dttm': times, 'titles': titles, 'themes': themes})
        df['dttm'] = f'{year}-{month}-{day} ' + df['dttm']

        print(df)

        df.to_csv(f'{name}.csv', index=False)
        return df

def test_0201():
  out_1 = html_parser_fontanka('2024','02','01','out_2') # dataframe
  out_1 = pd.read_csv('out_2.csv')
  true_df = pd.read_csv('out_1_real.csv')
  assert out_1.equals(true_df)

def test_0201_empt():
  out_2 = html_parser_fontanka('2027','02','01','out_2') # dataframe
  assert out_2 == None
  
