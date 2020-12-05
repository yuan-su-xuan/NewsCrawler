import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt


urlList=['https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E8%82%BA%E7%82%8E&oq=%25E6%25AD%25A6%25E6%25B1%2589%25E7%259C%2581&rsv_pq=c33d15c9000ac199&rsv_t=05eb4OY8uiVXgqqdCn5Yd0NOOyMPKx6ULxgsIQcE3GJeKTZfIBho200eSUA&rqlang=cn&rsv_dl=tb&rsv_enter=1&rsv_btype=t&inputT=6985&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1',
         'https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=20&oq=%E8%82%BA%E7%82%8E&ie=utf-8&usm=2&rsv_pq=95057cc600002864&rsv_t=1f7elVTGW8zcWyq9fbeeRg9WktBNBfpk9vXovqr5%2BDbXL8uMpDcJoxq8ZWo&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1']
findTitle=re.compile(r'target="_blank">(.*?)</a>')
findLink=re.compile(r'href="(.*?)"')
findSrc1=re.compile(r'<span class="nor-src-icon-v vicon-2"></span>(.*?)</a>')
findSrc2=re.compile(r'<div.*</div>(.*?)</a>')
findSrc3=re.compile(r'<a class="c-showurl c-color-gray" target="_blank" href=".*" style=".*">(.*?)</a>')
findTime=re.compile(r'<span class=.*>(.*?)\xa0</span>')

#得到指定url的网页源码、内容
def askUrl(url):
    #避免爬虫被认出非真人，告诉浏览器我们需要什么东西，模拟浏览器头部信息
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"}
    #request是一个库，Request是一个封装对象
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode('utf-8')
    except :
        print("error!")
        #返回源码
    return html
def getData():
    isMatch=False
    srclist=['网','报']
    dataList=[]
    for i in range(0,len(urlList)):
        url=urlList[i]
        html=askUrl(url)
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div', class_="result c-container new-pmd"):    #找到百度搜索结果的标题
            data=[]     #保存一个标题的信息
            item=str(item)
            SRC = re.findall(findSrc1, item)
            if len(SRC)==0:
                SRC=re.findall(findSrc2,item)
                if(len(SRC)==0):
                    SRC=re.findall(findSrc3,item)
                    if(len(SRC)==0):
                        continue
            src=SRC[0]
            #检验是否是来自于某个新闻网站的信息
            for keyWord in srclist:
                if keyWord in src:
                    # findall会返回所有结果的非重叠部分，如果有分组（即圆括号），则返回分组内容
                    title = re.findall(findTitle, item)[0].replace('<em>', '').replace('</em>', '')
                    link = re.findall(findLink, item)
                    time =re.findall(findTime,item)
                    data.append(src)
                    data.append(title)
                    data.append(link[0])
                    data.append(time[0])
                    dataList.append(data)
                    break

    return dataList
if __name__=='__main__':
    print(askUrl('https://www.baidu.com/s?wd=%E8%82%BA%E7%82%8E&pn=20&oq=%E8%82%BA%E7%82%8E&ie=utf-8&usm=2&rsv_pq=95057cc600002864&rsv_t=1f7elVTGW8zcWyq9fbeeRg9WktBNBfpk9vXovqr5%2BDbXL8uMpDcJoxq8ZWo&gpc=stf%3D1575475200%2C1579708799%7Cstftype%3D2&tfflag=1'))