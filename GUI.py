from tkinter import *
import CommentsGettter




text=Text()

def getFromGui(text):

    root = Tk()  # 建立tkinter窗口
    root.title("输入时间阶段获取信息")  # 设置标题
    Label(root, text='开始时间阶段：').grid(row=0, column=0)  # 选项row代表行，column代表列
    Label(root, text='结束时间阶段：').grid(row=1, column=0)
    Label(root, text='保存文件名：').grid(row=2, column=0)
    Label(root, text='爬取详情：').grid(row=3, column=0)
    # 输入框
    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    text=Text(root,width=30,height=10)
    # tkinter提供了三种布局组件的方式，第一种是pack()，第二种是Grid()网格，第三种是prase()
    # Grid允许我们使用表格的形式管理组件
    e1.grid(row=0, column=1, padx=10, pady=5)
    e2.grid(row=1, column=1, padx=10, pady=5)
    e3.grid(row=2, column=1, padx=10, pady=5)
    text.grid(row=3, column=1, padx=10, pady=5)
    Button(root, text='开始爬取数据', width=10, command=root.quit).grid(row=4, column=1, sticky=E, padx=10, pady=5)

    # 退出直接调用根窗口的quit方法
    mainloop()
    start = e1.get()
    end = e2.get()
    name = e3.get()
    CommentsGettter.getComments(start, end, name)



if __name__=='__main__':
    getFromGui(text)