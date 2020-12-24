import string
import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt
from urllib.parse import unquote, quote
import time
import random

keywordList = ['肺炎', '冠状病毒', '新冠', '不明传染', '疫情', '封城', '李文亮', '吹哨', '抗疫', '武汉领导']

baseUrlList1 = [
    # 由于第一阶段认识不足以及阶段性大事件未发生，仅有几个关键词有效
    # ‘肺炎’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%82%BA%E7%82%8E&advancedfilter=1&starttime=20191208&endtime=20200122&sort=hot&hasv=1&page=1',
    # ‘不明传染’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&advancedfilter=1&starttime=20191208&endtime=20200122&sort=ho&hasv=1t&page=1',
    # ‘冠状病毒’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&advancedfilter=1&starttime=20191208&endtime=20200122&sort=hot&hasv=1&page=1',
    # ‘发热’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%8F%91%E7%83%AD&advancedfilter=1&starttime=20191208&endtime=20200122&sort=hot&hasv=1&page=1',

]
baseUrlList2 = [
    # 抗疫
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%8A%97%E7%96%AB&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 不明传染
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 肺炎
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%82%BA%E7%82%8E&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 新冠
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%96%B0%E5%86%A0&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 疫情
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E7%96%AB%E6%83%85&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 李文亮
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%9D%8E%E6%96%87%E4%BA%AE&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 吹哨
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%90%B9%E5%93%A8&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 封城
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%B0%81%E5%9F%8E&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
    # 武汉
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%AD%A6%E6%B1%89&advancedfilter=1&starttime=20200123&endtime=20200207&sort=hot&hasv=1&page=1',
]
baseUrlList3 = [
    # 吹哨
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%90%B9%E5%93%A8&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 抗疫
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%8A%97%E7%96%AB&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 肺炎
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%82%BA%E7%82%8E&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 冠状病毒
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 封城
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%B0%81%E5%9F%8E&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 新冠
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%96%B0%E5%86%A0&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 疫情
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E7%96%AB%E6%83%85&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # 李文亮
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%9D%8E%E6%96%87%E4%BA%AE&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    # ‘武汉’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%AD%A6%E6%B1%89&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=1',
    #武汉领导
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%AD%A6%E6%B1%89%E9%A2%86%E5%AF%BC&advancedfilter=1&starttime=20200208&endtime=20200309&sort=hot&hasv=1&page=6',
]
baseUrlList4 = [
    # ‘肺炎’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E8%82%BA%E7%82%8E&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘冠状病毒’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘新冠’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%96%B0%E5%86%A0&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘疫情’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E7%96%AB%E6%83%85&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘抗疫’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%8A%97%E7%96%AB&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘李文亮’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E6%9D%8E%E6%96%87%E4%BA%AE&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    # ‘封城’
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%B0%81%E5%9F%8E&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=1',
    #复工
    'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%A4%8D%E5%B7%A5&advancedfilter=1&starttime=20200310&endtime=20200615&sort=hot&hasv=1&page=2',


]
findId = re.compile(r'M_I.*')
findSrc = re.compile(r'<a.*>(.*?)</a>')
findHref=re.compile(r'<a class="cc" href="(.*?)">')
findNum=re.compile(r'\[(.*?)\]')

workbook = xlwt.Workbook('微博新闻.xls')
lineCount = 1


# 得到指定url的网页源码、内容
def askUrl(url):
    # 避免爬虫被认出非真人，告诉浏览器我们需要什么东西，模拟浏览器头部信息
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Cookie": 'SCF=Apz6fSHB1thzITfS8Nak59eNU6qB_SFo-EciuEFPTD-ryXQSZPfv3LZNxdwKz2oTWF0k-uJZFtbqGkM3IBkMhiM.; SUB=_2A25y53o8DeRhGeNL7lUR8inIzjuIHXVuKAZ0rDV6PUJbktANLVLtkW1NSO5r6BczU-QqD6pt0UKuGpmoEDVpxphP; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhNX3Kq-cB_kdnY9aN0MY0Z5NHD95QfSK-NehzNSh-NWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSK-fS05ES0BfS7tt; _T_WM=ef6273c0266369569ff1c11e3c15107b; SSOLoginState=1608714860',
            'Host': 'weibo.cn',
            'Connection': 'keep-alive'}

    url = quote(url, safe=string.printable)
    # request是一个库，Request是一个封装对象
    request = urllib.request.Request(url, headers=head)

    html = ""
    try:
        time.sleep(random.random())
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except:
        html = None
        print("error!")
        # 返回源码
    return html


dataList = []


def getData(baseUrl):
    srclist = ['网', '报', '新闻', '播', '观察', '社', '在线', '观', '中国', '法', '共青', '青年', '中央', 'CCTV', '检察', '观察']

    for i in range(0, 100):
        url = baseUrl.replace('page=1', 'page=' + str(i + 1))
        html = askUrl(url)
        if html == None:
            break
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', {'class': 'c', 'id': findId}):  # 找到一条微博
            print('进入了一个段里')
            data = []  # 保存一个标题的信息
            name = item.find_all('a', {'class': 'nk'})[0]
            name = re.findall(findSrc, str(name))[0]
            p = item.find_all('span', {'class': 'ctt'})
            p = p[0].text.strip()
            time = item.find_all('span', {'class': 'ct'})[0].text.strip()

            # 检验是否是来自于某个新闻网站的信息
            for keyWord in srclist:
                if keyWord in name:
                    isMatch = True
                    commentHrefTotal = item.find_all('a', {'class': 'cc'})[0]
                    commentCount=int(re.findall(findNum,commentHrefTotal.text)[0])
                    if commentCount <10:
                        break
                    commentHref = commentHrefTotal['href']
                    comments = getComment(commentHref)
                    data.append(name)
                    data.append(time)
                    data.append(p)
                    for i in range(0,len(comments)):
                        data.append(comments[i])
                    if isMatch and (data not in dataList):
                        dataList.append(data)
                        print('datalist中增加了第' + str(len(dataList)) + '条数据')
                    break


def savaData(dataList, sheetName):
    # 创建workbook对象
    global lineCount
    wordsheet = workbook.add_sheet(sheetName, cell_overwrite_ok=True)  # 创建工作表
    col = ('来源', '时间', '内容', '评论')
    for i in range(0, 4):
        wordsheet.write(0, i, col[i])  # 第一个参数为行，第二个为列，第三个为写入的数据
    for i in range(0, len(dataList)):
        data = dataList[i]
        for j in range(0, len(data)):
            wordsheet.write(lineCount, j, data[j])
        print(sheetName + '写入了第', lineCount, '条数据')
        lineCount = lineCount + 1

    workbook.save('第二阶段.xls')

def getComment(commentHref):
    commentHtml=askUrl(commentHref)
    soup = BeautifulSoup(commentHtml, "html.parser")
    spanTotal=soup.find_all('span',{'class': "ctt",})
    commentList=[]
    for i in range(1,len(spanTotal)):
        commentList.append(spanTotal[i].text)
    return commentList

def getHotComments(hotUrl):
    commentList = []
    hotHtml=askUrl(hotUrl)
    soup = BeautifulSoup(hotHtml, "html.parser")
    i=0
    for item in soup.find_all('span', {'class': 'ctt'}):

        if i <1:
            i = i + 1
            continue
        commentList.append(item.text)
        i = i + 1
        if i ==6:
            break
    return commentList


if __name__ == '__main__':
    dataList = []
    for i in range(0, len(baseUrlList3)):
        getData(baseUrlList3[i])
    savaData(dataList, '第三阶段')

