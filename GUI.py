from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import CommentsGettter
import analysis
from picture import picture

url = "./pic/linechart.png"
root = Tk()  # 建立tkinter窗口
root.title("公众情绪心态分析")  # 设置标题
condition=False
PIC1=picture(root)
PIC2=picture(root)
PIC3=picture(root)
PIC4=picture(root)
PIC5=picture(root)
PIC6=picture(root)
def counter(btn):  # 增加一个参数把button对象传入，用来更改它的文字
    global condition
    messagebox.showinfo("注意", "正在分析数据，请稍等...")
    #startData()
    messagebox.showinfo("注意", "数据分析已完成！ 分析图片存于pic文件夹中!")
    label1.destroy()
    e1.destroy()
    label2.destroy()
    e2.destroy()
    label3.destroy()
    e3.destroy()
    btn.destroy()
    quit.grid(row=6, column=2, sticky=E, padx=10, pady=5)
    findImg()

label1=Label(root, text='开始时间阶段：')
label1.grid(row=0, column=0) # 选项row代表行，column代表列
label2=Label(root, text='结束时间阶段：')
label2.grid(row=1, column=0)
label3=Label(root, text='保存文件名：')
label3.grid(row=2, column=0)
label=None
# 输入框
e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)
# tkinter提供了三种布局组件的方式，第一种是pack()，第二种是Grid()网格，第三种是prase()
# Grid允许我们使用表格的形式管理组件
e1.grid(row=0, column=1, padx=10, pady=5)
e2.grid(row=1, column=1, padx=10, pady=5)
e3.grid(row=2, column=1, padx=10, pady=5)
button = Button(root, text='开始分析数据', width=10, command=lambda :counter(button))
button.grid(row=5, column=0, sticky=E, padx=10, pady=5)
quit=Button(root, text='退出', width=10, command=root.quit)
quit.grid(row=6, column=0, sticky=E, padx=10, pady=5)

def startData():
    start = e1.get()
    end = e2.get()
    name = e3.get()
    CommentsGettter.getComments(start, end, name)
    analysis.analysis(name+".xls")
def findImg():
    url1="./pic/linechart.png"
    PIC1.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC1.img = ImageTk.PhotoImage(PIC1.pil_image)
    PIC1.label_img.configure(image=PIC1.img)
    PIC1.label_img.grid(column=0, row=0, sticky=W)
    url1="./pic/local_linechart.png"
    PIC2.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC2.img = ImageTk.PhotoImage(PIC2.pil_image)
    PIC2.label_img.configure(image=PIC2.img)
    PIC2.label_img.grid(column=1, row=0, sticky=W)
    url1="./pic/piechart1.png"
    PIC3.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC3.img = ImageTk.PhotoImage(PIC3.pil_image)
    PIC3.label_img.configure(image=PIC3.img)
    PIC3.label_img.grid(column=2, row=0, sticky=W)
    url1="./pic/piechart2.png"
    PIC4.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC4.img = ImageTk.PhotoImage(PIC4.pil_image)
    PIC4.label_img.configure(image=PIC4.img)
    PIC4.label_img.grid(column=0, row=1, sticky=W)
    url1="./pic/piechart3.png"
    PIC5.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC5.img = ImageTk.PhotoImage(PIC5.pil_image)
    PIC5.label_img.configure(image=PIC5.img)
    PIC5.label_img.grid(column=1, row=1, sticky=W)
    url1="./pic/piechart4.png"
    PIC6.pil_image = Image.open(url1).resize((300, 300), Image.ANTIALIAS)
    PIC6.img = ImageTk.PhotoImage(PIC6.pil_image)
    PIC6.label_img.configure(image=PIC6.img)
    PIC6.label_img.grid(column=2, row=1, sticky=W)
    #root.update_idletasks()   #更新图片，必须update
if __name__=='__main__':
    mainloop()