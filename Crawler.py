import string
import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt
from urllib.parse import unquote, quote
import time
keywordList = ['肺炎', '冠状病毒', '新冠', '不明传染', '疫情', '封城', '李文亮', '吹哨', '抗疫', '武汉领导']

baseUrlList1 = [
    # 由于第一阶段认识不足以及阶段性大事件未发生，仅有几个关键词有效
    #‘不明传染’
    'https://www.baidu.com/s?wd=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&pn=0&oq=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&ie=utf-8&usm=3&rsv_pq=f922dd970003ed14&rsv_t=204eRpbQnGiUzhIHu3D%2BuiC1mdz7d8hoAAijN%2BQ3ozFjB4GBIubdTbyHacc&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
    #‘肺炎’
    'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=0&oq=%E8%82%BA%E7%82%8E&ie=utf-8&usm=2&rsv_pq=95057cc600002864&rsv_t=1f7elVTGW8zcWyq9fbeeRg9WktBNBfpk9vXovqr5%2BDbXL8uMpDcJoxq8ZWo&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
    #‘冠状病毒’
    'https://www.baidu.com/s?wd=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&pn=0&oq=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&ie=utf-8&rsv_pq=b211c8a700014499&rsv_t=2b6bmZTLo6GCdF%2B%2FnMEaW0mwCEI3WtAsm2b4WKe62T91thIigeu1e%2FED1Y4&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
    #‘不明发热’
    'https://www.baidu.com/s?wd=%E4%B8%8D%E6%98%8E%E5%8F%91%E7%83%AD&pn=0&oq=%E4%B8%8D%E6%98%8E%E5%8F%91%E7%83%AD&ie=utf-8&rsv_pq=cde9b2a900069af9&rsv_t=569fYW1waSku8LHdGUvPzfIsaYP8u1TF%2FcEDts87Ai8SbbKsz4xs5Eiki9A&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',


]
baseUrlList2 = [
    #不明传染
    'https://www.baidu.com/s?wd=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&pn=0&oq=%E4%B8%8D%E6%98%8E%E4%BC%A0%E6%9F%93&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #肺炎
    'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=0&oq=%E8%82%BA%E7%82%8E&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #新冠
    'https://www.baidu.com/s?wd=%E6%96%B0%E5%86%A0&pn=0&oq=&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #疫情
    'https://www.baidu.com/s?wd=%E7%96%AB%E6%83%85&pn=0&oq=&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #李文亮
    'https://www.baidu.com/s?wd=%E6%9D%8E%E6%96%87%E4%BA%AE&pn=0&oq=&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #吹哨
    'https://www.baidu.com/s?wd=%E5%90%B9%E5%93%A8&pn=0&oq=&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #抗疫
    'https://www.baidu.com/s?wd=%E6%8A%97%E7%96%AB&pn=0&oq=&ie=utf-8&rsv_pq=a0f0ed4e000057a1&rsv_t=bf5cI%2FkJ5NUZLOoyArEF0bIh7aNy%2FWMQUN6HKkdlipPNEm8Vr%2FWvh8ToZts&gpc=stf%3D1579708800%2C1581091199%7Cstftype%3D2&tfflag=1',
    #‘封城’
    'https://www.baidu.com/s?wd=%E5%B0%81%E5%9F%8E&pn=0&oq=%E5%B0%81%E5%9F%8E&ie=utf-8&rsv_pq=dedfb29200006ca9&rsv_t=10beIAoXRImN3RvxAB91L7BX%2FNOa0V6ctuTd5mPX0EFBJlWYWOuIOm02unQ&gpc=stf%3D1579708800%2C1581263999%7Cstftype%3D2&tfflag=1',

]
baseUrlList3 = [
    # 在这个阶段‘不明传染’关键字只会搜索到国外疫情，与本次主题无关，故该list不包含这个关键词
    #吹哨
    'https://www.baidu.com/s?wd=%E5%90%B9%E5%93%A8&pn=0&oq=%E5%90%B9%E5%93%A8&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #抗疫
    'https://www.baidu.com/s?wd=%E6%8A%97%E7%96%AB&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #肺炎
    'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #冠状病毒
    'https://www.baidu.com/s?wd=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #封城
    'https://www.baidu.com/s?wd=%E5%B0%81%E5%9F%8E&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #新冠
    'https://www.baidu.com/s?wd=%E6%96%B0%E5%86%A0&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #疫情
    'https://www.baidu.com/s?wd=%E7%96%AB%E6%83%85&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    #李文亮
    'https://www.baidu.com/s?wd=%E6%9D%8E%E6%96%87%E4%BA%AE&pn=0&oq=&ie=utf-8&rsv_pq=8aca3efe0000ba77&rsv_t=b38bqSkRVsU6FFBDrPsTwSHmFkUAZ57HEonygu5w3qBNoaX06TgWdUhYOYo&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',
    # ‘武汉领导’
    'https://www.baidu.com/s?wd=%E6%AD%A6%E6%B1%89%E9%A2%86%E5%AF%BC&pn=0&oq=%E6%AD%A6%E6%B1%89%E9%A2%86%E5%AF%BC&ie=utf-8&rsv_pq=bd945c2c00004cfe&rsv_t=1a54Zq%2BxrQzpacR59j5ATH336UciZ%2FVJPXNUwH4vazwJvHf2YYb1ORyFiDs&gpc=stf%3D1581264000%2C1583769599%7Cstftype%3D2&tfflag=1',

]
baseUrlList4 = [
    # ‘肺炎’
    'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘冠状病毒’
    'https://www.baidu.com/s?wd=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&pn=0&oq=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘新冠’
    'https://www.baidu.com/s?wd=%E6%96%B0%E5%86%A0&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘疫情’
    'https://www.baidu.com/s?wd=%E7%96%AB%E6%83%85&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘抗疫’
    'https://www.baidu.com/s?wd=%E6%8A%97%E7%96%AB&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘吹哨’
    'https://www.baidu.com/s?wd=%E5%90%B9%E5%93%A8&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘李文亮’
    'https://www.baidu.com/s?wd=%E6%9D%8E%E6%96%87%E4%BA%AE&pn=0&oq=&ie=utf-8&rsv_pq=9fa7013600000b6b&rsv_t=5ff5MjUOealYwwHTM2iKMjyxMQZOJEhGfGnNeBsfrom2izVQJwOg66njR2o&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',
    # ‘封城’
    'https://www.baidu.com/s?wd=%E5%B0%81%E5%9F%8E&pn=0&oq=%E5%B0%81%E5%9F%8E&ie=utf-8&rsv_pq=88a29ad000009e8a&rsv_t=70401nkEEm55acjeiktius1lKUumUK6DeLKwuFJZZrvW6rYVwQaV9jJjx8w&gpc=stf%3D1583769600%2C1592841599%7Cstftype%3D2&tfflag=1',

]
findTitle = re.compile(r'target="_blank">(.*?)</a>')
findLink = re.compile(r'href="(.*?)"')
findSrc1 = re.compile(r'<span class="nor-src-icon-v vicon-2"></span>(.*?)</a>')
findSrc2 = re.compile(r'<div.*</div>(.*?)</a>')
findSrc3 = re.compile(r'tar"><a class="c-showurl c-color-gray" href=".*" style="text-decoration:none;position:relative;" target="_blank">(.*?)</a><div class="c-tools c-gap-left"')
findTime = re.compile(r'<span class=.*>(.*?)\xa0</span>')


workbook = xlwt.Workbook(encoding='utf-8')
lineCount = 1


# 得到指定url的网页源码、内容
def askUrl(url):
    # 避免爬虫被认出非真人，告诉浏览器我们需要什么东西，模拟浏览器头部信息
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    url = quote(url, safe=string.printable)
    # request是一个库，Request是一个封装对象
    request = urllib.request.Request(url, headers=head)
    time.sleep(1)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except:
        print("error!")
        # 返回源码
    return html

dataList=[]
def getData(baseUrl):

    srclist = ['网', '报', '新闻', '播', '观察', 'news', '社', '在线']

    for i in range(0, 40):
        page = str(10 * i)
        url = baseUrl.replace('pn=0', 'pn=' + page)
        html = askUrl(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="result c-container new-pmd"):  # 找到百度搜索结果的标题
            print('进入了一个段里')
            data = []  # 保存一个标题的信息
            item = str(item)
            SRC = re.findall(findSrc1, item)
            if len(SRC) == 0:
                SRC = re.findall(findSrc2, item)
                if (len(SRC) == 0):
                    SRC = re.findall(findSrc3, item)
                    if (len(SRC) == 0):
                        continue

            src = SRC[0]
            # 筛选掉由于正则不精确导致的误选
            if 'class' in src or '健康' in src or '医' in src or '视频' in src or '电影' in src or '药' in src:
                continue

            # 检验是否是来自于某个新闻网站的信息
            for keyWord in srclist:
                if keyWord in src:
                    isMatch=True
                    # findall会返回所有结果的非重叠部分，如果有分组（即圆括号），则返回分组内容
                    title = re.findall(findTitle, item)[0].replace('<em>', '').replace('</em>', '')
                    link = re.findall(findLink, item)
                    time = re.findall(findTime, item)
                    data.append(src)
                    data.append(title)
                    data.append(link[0])
                    if (len(time) != 0):
                        data.append(time[0])
                    else:
                        data.append('未标明确切来源时间')
                    for i in range(0,len(dataList)):
                        if title ==dataList[i][1]:
                            isMatch=False
                            break
                    if isMatch:
                        dataList.append(data)
                        print('datalist中增加了第'+str(len(dataList))+'条数据')




def savaData(dataList, sheetName):
    # 创建workbook对象
    global lineCount
    wordsheet = workbook.add_sheet(sheetName, cell_overwrite_ok=True)  # 创建工作表
    col = ('来源', '新闻标题', '新闻链接', '新闻发布时间')
    for i in range(0, 4):
        wordsheet.write(0, i, col[i])  # 第一个参数为行，第二个为列，第三个为写入的数据
    for i in range(0, len(dataList)):
        data = dataList[i]
        for j in range(0, 4):
            wordsheet.write(lineCount, j, data[j])
        print(sheetName + '写入了第', lineCount, '条数据')
        lineCount = lineCount + 1

    workbook.save('新冠疫情新闻总表.xls')


if __name__ == '__main__':
    dataList=[]
    for i in range(0,len(baseUrlList1)):
        getData(baseUrlList1[i])
    savaData(dataList,'第一阶段')
    dataList=[]
    lineCount=1
    for i in range(0, len(baseUrlList2)):
        getData(baseUrlList2[i])
    savaData(dataList, '第二阶段')
    dataList=[]
    lineCount=1
    for i in range(0, len(baseUrlList3)):
        getData(baseUrlList3[i])
    savaData(dataList, '第三阶段')
    dataList=[]
    lineCount=1
    for i in range(0, len(baseUrlList4)):
        getData(baseUrlList4[i])
    savaData(dataList, '第四阶段')

