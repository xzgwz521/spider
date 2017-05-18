# -*- coding: utf-8 -*-
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
        print('总页数为 %d' % number)
        return number


def get_img_urls(page):  # 获取当前页面的所有图片地址，返回列表
    img_srcs = []
    page_url = 'http://www.meizitu.com/' + '/a/' + str(page) + '.html'
    html = url_open(page_url)
    soup = BeautifulSoup(html, "lxml")
    img_div = soup.find_all('div', id="picture")
    img_soup = BeautifulSoup(str(img_div), "lxml")  # 返回的列表长度为1
    img_result = list(img_soup.find_all('img'))  # 返回的列表长度为图片数
    img_url = re.compile('http:.*\.jpg')
    for each in img_result:
        m = re.search(img_url, str(each))
        if m:
            img_src = str(m.group())
            img_srcs.append(img_src)

    return img_srcs  # 返回图片链接的列表


def save_img(img_srcs, current_page):
    a = random.random()  # 设置0-1秒的随机时间，用作延时
    count = 0  # 当前页面图片计数
    for each in img_srcs:
        filename = str(current_page) + '-'+str(count+1) + '.jpg'
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            if size == 0:
                print('重新下载 %s' % filename)
                with open(filename, 'wb') as f:
                    picture = url_open(each)
                    f.write(picture)
            count += 1
            print('第 %d 页的第 %d 张图片 %s 已存在，跳过' % (current_page, count, filename))
            time.sleep(a)
        else:
            with open(filename, 'wb') as f:
                picture = url_open(each)
                f.write(picture)
            count += 1
            print('已下载第 %d 页的第 %d 张图片,文件名为 %s ' % (current_page, count, filename))
            time.sleep(a*2)

    return count


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
    total_num = 0  # 初始化下载图片总个数
    a = random.random()
    for p in range(0, total_page):
        current_page = total_page-p  # 当前下载页面的页数
        img_srcs = get_img_urls(current_page)  # 获取当前下载页面所有图片的链接， 类型为列表
        count = save_img(img_srcs, current_page)
        total_num += count
        print('当前已下载图片总数为： %d ' % total_num)
        time.sleep(a*3)


if __name__ == '__main__':
    download()
