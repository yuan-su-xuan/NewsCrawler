from tkinter import*

from PIL import Image, ImageTk

url = "./pic/linechart.png"
class picture:
    def __init__(self,root):
        self.pil_image = Image.open(url)
        self.pil_image = self.pil_image.resize((600, 600), Image.ANTIALIAS)
        self.img =ImageTk.PhotoImage(self.pil_image)
        self.label_img = Label(root, image=self.img)


#root = Tk()
#pic=picture(root)
#mainloop()