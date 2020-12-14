import xlrd
import xlwt
from bs4 import BeautifulSoup
import time
import Crawler

workbook = xlwt.Workbook('新闻内容.xls')


def getNews(xlsPath):
    readbook = xlrd.open_workbook(xlsPath)
    for i in range(0, 4):
        sheet = readbook.sheet_by_index(i)
        writeText(i, sheet)
        workbook.save('新闻内容')
        time.sleep(60)

def writeText(i, sheet):
    toWriteSheet = workbook.add_sheet("第" + str(i) + "阶段", cell_overwrite_ok=True)
    nrows = sheet.nrows
    row = 0
    for i in range(1, nrows):
        name = sheet.cell(i, 1).value
        url = sheet.cell(i, 2).value
        text = getText(url)
        if text == None:
            print('跳过无效url')
            continue
        toWriteSheet.write(row, 0, name)
        toWriteSheet.write(row, 1, text)
        print('第'+str(row)+'行已被读入')
        row += 1



def getText(url):
    html = Crawler.askUrl(url)
    if html == None:
        return None
    soup = BeautifulSoup(html, "html.parser")
    contents = soup.find_all('span', {'class': 'bjh-p'})
    if len(contents) == 0:
        contents = soup.find_all('p')
    text = ''
    for i in range(0, len(contents)):
        text += contents[i].text
    return text


if __name__ == '__main__':
    getNews('E:\python文件\MyCrawler\新冠疫情新闻.xls')
