# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl

def crawl_request():
    pattern = re.compile("\d+\.\d+")
    arr_titles = []
    arr_views = []
    arr_counts = []
    arr_authors = []
    arr_thumbnails = []

    req = requests.get("https://howkteam.vn/learn")
    soup = BeautifulSoup(req.content, "html.parser")
    try:
        titles = soup.findAll('h4', class_='font-size-default font-w600 mb-10 text-overflow-dot')
        for i in titles:
            arr_titles.append(i.text)
        # print(arr_titles)

        total = soup.findAll('div', class_='d-inline-block')
        for i in total:
            v = i.findChildren('strong', recursive=False)
            if v:
                a = v[0].text
                b = re.findall(pattern, a)
                if b:
                    arr_views = arr_views + b
                else:
                    arr_counts.append(a)
        # print(arr_views)
        # print(arr_counts)

        authors = soup.findAll('div', class_='block-content block-content-full useravatar-edit-container')
        for i in authors:
            a = i.findChildren('a', recursive=False)
            arr_author = []
            if a:
                for au in a:
                    splits = au.text.split("\n")
                    author = [x for x in splits if x]
                    arr_author = arr_author + author
                arr_authors.append(arr_author)
        # print(arr_authors)

        imgs = soup.findAll('img', class_='img-fluid options-item w-100')
        for i in imgs:
            arr_thumbnails.append(i.attrs['src'])
        # print(arr_thumbnails)

        fields = ['Tieu de', 'Luot xem', 'Bai hoc', 'Tac gia', 'Thumbnail']
        df = pd.DataFrame(list(zip(*[arr_titles, arr_views, arr_counts, arr_authors, arr_thumbnails])), columns=fields)
        print(df)
        with pd.ExcelWriter("kteam_req.xlsx") as writer:
            df.to_excel(writer)

    except Exception as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    crawl_request()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
