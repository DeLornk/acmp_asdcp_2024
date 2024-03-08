from bs4 import BeautifulSoup
import requests
import argparse
from pandas import DataFrame

parser = argparse.ArgumentParser(description='Парсим новости с fontanka.ru')
parser.add_argument('year', type=str, help='Год в формате: xxxx. Например, 2024')
parser.add_argument('month', type=str, help='Год в формате: xx. Например, 07')
parser.add_argument('day', type=str, help='Год в формате: xx. Например, 07')
parser.add_argument('name', type=str, help='Название csv файла для сохранения')

args = parser.parse_args()

html_text = requests.get(rf'https://www.fontanka.ru/{args.year}/{args.month}/{args.day}/all.html').text
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

if len(times) == 0:
    print(f"Ничего не было найдено за дату {args.year}-{args.month}-{args.day}")
    print("Либо такой страницы не существуют, либо на сайте были изменены классы элементов")
else:
    print(f"Найдено: {len(times)} новостей")

    df = DataFrame({'dttm': times, 'titles': titles, 'themes': themes})
    df['dttm'] = f'{args.year}-{args.month}-{args.day} ' + df['dttm']

    print(df)

    df.to_csv(f'{args.name}.csv', index=False)
