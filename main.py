import sys
import time
import io

import requests
import xlrd
from bs4 import BeautifulSoup


# 判断是否能访问；获取标题；进行报错处理
def exception(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.88 Safari/537.36'}
        r = requests.get(url=url, headers=headers, timeout=5)
        if r.apparent_encoding == 'utf-8':
            r.encoding = 'utf-8'
        time.sleep(0.01)
        if r.status_code == 200:
            html = BeautifulSoup(r.text, "lxml")
            html.prettify()
            if html.title is None:
                title = 'null'
            elif html.title.string is None:
                title = 'null'
            else:
                title = html.title.string.replace(' ', '').replace('\t', '').replace('\n', '')

            # title = title.encode(('utf-8'))
            print(title)
            print(url + '\t\t\t\t\t\t' + "成功访问")
            print("===========================================================")

        elif r.status_code == 418:
            print(url + '\n' + "++++++++++触发了反爬虫+++++++++++")
        else:
            time.sleep(2)
            print(url + '\t访问页面出错 Error:', r.status_code)
            print("===========================================================")

    except requests.exceptions.Timeout:
        time.sleep(2)
        print(url + '\t 连接、读取超时')
        print("===========================================================")

    except requests.exceptions.ConnectionError:
        time.sleep(2)
        print(url + '\t 未知的服务器')
        print("===========================================================")



# 格式化url
def urls(lines):
    for line in lines:
        # 判断是否为空
        if line:
            line = line.replace(' ', '').replace('\t', '').replace('\n', '').lower()
            if line[0:4] == 'http':
                exception(line)
            else:
                url_h = 'http://' + line
                exception(url_h)
                url_hs = 'https://' + line
                exception(url_hs)
        else:
            print("++空行++")


if __name__ == '__main__':
    work_book = xlrd.open_workbook('D:/识别网页情况/企业网址列表.xlsx')
    sheet_1 = work_book.sheet_by_name('Sheet1')
    # 读取一整列的数据

    # row_data = sheet_1.row_values(1)  
    # print(row_data[5])  

    lie = [str(sheet_1.cell_value(i, 2)) for i in range(1, sheet_1.nrows)]
    urls(lie)
    # r = requests.get(url, timeout=5)
    #
    # r.encoding = 'utf-8'
    # code = r.status_code
    # html = BeautifulSoup(r.text)
    # s = html.title.string
    # print(s)
    # if code == 200:
    #     print("网站访问正常")
    #     sys.exit(0)
    # else:
    #     print("不能访问 Error:", code)

    # file = open('test.txt')
    # lines = file.readlines()
    # print('开始检查：\nurl\t标题')
    # urls(lines)
    # file.close()
