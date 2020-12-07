import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt

keywordList = ['肺炎', '冠状病毒', ]
lineCount = 1
baseUrlList = [
    'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=0&oq=%E8%82%BA%E7%82%8E&ie=utf-8&usm=2&rsv_pq=95057cc600002864&rsv_t=1f7elVTGW8zcWyq9fbeeRg9WktBNBfpk9vXovqr5%2BDbXL8uMpDcJoxq8ZWo&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
    'https://www.baidu.com/s?wd=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&pn=0&oq=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&ie=utf-8&rsv_pq=b211c8a700014499&rsv_t=2b6bmZTLo6GCdF%2B%2FnMEaW0mwCEI3WtAsm2b4WKe62T91thIigeu1e%2FED1Y4&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
    'https://www.baidu.com/s?wd=%E5%8F%91%E7%83%AD%E7%97%85%E4%BE%8B&pn=0&oq=%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92&ie=utf-8&rsv_pq=b211c8a700014499&rsv_t=2b6bmZTLo6GCdF%2B%2FnMEaW0mwCEI3WtAsm2b4WKe62T91thIigeu1e%2FED1Y4&gpc=stf%3D1575475200%2C1579708799|stftype%3D2&tfflag=1',
]
findTitle = re.compile(r'target="_blank">(.*?)</a>')
findLink = re.compile(r'href="(.*?)"')
findSrc1 = re.compile(r'<span class="nor-src-icon-v vicon-2"></span>(.*?)</a>')
findSrc2 = re.compile(r'<div.*</div>(.*?)</a>')
findSrc3 = re.compile(r'<a class="c-showurl c-color-gray" target="_blank" href=".*" style=".*">(.*?)</a>')
findTime = re.compile(r'<span class=.*>(.*?)\xa0</span>')

dataList = []
workbook = xlwt.Workbook(encoding='utf-8')


# 得到指定url的网页源码、内容
def askUrl(url):
    # 避免爬虫被认出非真人，告诉浏览器我们需要什么东西，模拟浏览器头部信息
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    # request是一个库，Request是一个封装对象
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except:
        print("error!")
        # 返回源码
    return html


def getData(baseUrl):
    srclist = ['网', '报', '新闻', '播']

    for i in range(0, 14):
        page = str(10 * i)
        url = baseUrl.replace('pn=0', 'pn=' + page)
        html = askUrl(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="result c-container new-pmd"):  # 找到百度搜索结果的标题
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
            # 检验是否是来自于某个新闻网站的信息
            for keyWord in srclist:
                if keyWord in src:
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
                    if data not in dataList:
                        dataList.append(data)


def savaData(dataList):
    # 创建workbook对象
    global lineCount
    wordsheet = workbook.add_sheet('第一阶段', cell_overwrite_ok=True)  # 创建工作表
    col = ('来源', '新闻标题', '新闻链接', '新闻发布时间')
    for i in range(0, 4):
        wordsheet.write(0, i, col[i])  # 第一个参数为行，第二个为列，第三个为写入的数据
    for i in range(0, len(dataList)):
        data = dataList[i]
        for j in range(0, 4):
            wordsheet.write(lineCount, j, data[j])
            lineCount = lineCount + 1
    workbook.save('新冠疫情新闻总表.xls')

if __name__ == '__main__':
    for i in range(0, len(baseUrlList)):
        getData(baseUrlList[i])
    savaData(dataList)
