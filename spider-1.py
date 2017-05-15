import urllib.request
import os
import re
from bs4 import BeautifulSoup
import time
import random


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; \
    Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 \
    Safari/537.36')
    html = urllib.request.urlopen(req).read()

    return html


def get_total_page(html):  # 获取总页数
    soup = BeautifulSoup(html, "lxml")
    first_page = soup.find('div', id="picture").find('a').get('href')
    n = re.search(r'[0-9]{1,10}', first_page)
    if n:
        number = int(n.group())
        return number


def get_img_urls(page):  # 获取第二页的所有图片地址，返回列表
    img_srcs = []
    page_url = 'http://www.meizitu.com/' + '/a/' + str(page) + '.html'
    html = url_open(page_url)
    soup = BeautifulSoup(html, "lxml")
    img_div = soup.find_all('div', id="picture")
    img_soup = BeautifulSoup(str(img_div), "lxml")  # 返回的列表长度为1
    img_result = list(img_soup.find_all('img'))  # 返回的列表长度为图片数
    for each in img_result:
        img_url = re.compile('http:.*\.jpg')
        m = re.search(img_url, str(each))
        if m:
            img_src = str(m.group())
            img_srcs.append(img_src)

    return img_srcs


def download():
    folder = 'picture'
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)

    url = 'http://www.meizitu.com/'
    html = url_open(url)
    total_page = get_total_page(html)
    print('总页面为 %d' % total_page)
    total_num = 0
    for page in range(0, total_page):
        img_srcs = get_img_urls(total_page-page)
        count = 0
        for each in img_srcs:
            filename = str(total_page-page) + '-'+str(count+1) + '.jpg'
            with open(filename, 'wb') as f:
                picture = url_open(each)
                f.write(picture)
            count += 1

            print('已下载第 %d 页的第 %d 张图片,文件名为 %s ' % (total_page-page, count, filename))
        total_num += count
        print('当前一共下载了 %d 张图片' % total_num)
        a = random.random() * 3
        time.sleep(a)


if __name__ == '__main__':
    download()
