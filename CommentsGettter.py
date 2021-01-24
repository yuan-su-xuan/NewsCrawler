import WeiBoCrawler
import re

stime=re.compile(r'starttime=[0-9]*')
etime=re.compile(r'endtime=[0-9]*')
#设置爬取新闻的时间段
def setTime(starttime,endtime,baseUrlList):

    list=[]
    for url in baseUrlList:
        toReplace1=re.findall(stime,url)[0]
        toReplace2=re.findall(etime,url)[0]
        url=url.replace(toReplace1,'starttime='+str(starttime)).replace(toReplace2,'endtime='+str(endtime))
        print(url)
        list.append(url)
    return list

def getComments(starttime,endtime,workbookName):
    baseUrlList = WeiBoCrawler.baseUrlList5
    baseUrlList=setTime(starttime,endtime,baseUrlList)
    for i in range(0, len(baseUrlList)):
        WeiBoCrawler.getData(baseUrlList[i])
    #最后存储的工作表名字就是第二个参数
    WeiBoCrawler.savaData(WeiBoCrawler.dataList,workbookName)