import time
from PIL import ImageGrab
import tkinter as tk
import os
import win32clipboard
from PIL import Image
from io import BytesIO
import TextRecognize
class FreeScreenShot():
    def __init__(self,root,img):
        
        """保存鼠标左键点击位置（一会要赋值的）"""
        self.X = tk.IntVar(value = 0)
        self.Y = tk.IntVar(value = 0)

        """获取屏幕尺寸"""
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        ### 顶级组件容器

        self.top = tk.Toplevel(root,width=screenWidth,height = screenHeight)

        ### 隐藏顶条
        self.top.overrideredirect(True)
        self.canvas = tk.Canvas(self.top,bg = 'white',width = screenWidth,height = screenHeight)

        ### 显示全屏截图，然后进行区域截图
        self.image = tk.PhotoImage(file = img)
        self.canvas.create_image(screenWidth//2,screenHeight//2,image = self.image)

        self.lastDraw = None

        """更新鼠标左键按下位置"""
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.begin = True

        self.canvas.bind('<Button-1>',onLeftButtonDown)# 绑定按键和事件

        """鼠标移动选取区域"""
        def onLeftButtonMove(event):
            #鼠标左键移动，显示选取的区域
            if not self.begin:
                return
            try: #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass
            self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='green')

        """鼠标左键抬起，完成截图"""
        def onLeftButtonUp(event):
            #获取鼠标左键抬起的位置，保存区域截图
            self.begin = False
            try:
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass

            time.sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            self.pic = pic  ## 存下图片
            pic.save("temp2.png")
            I2T = TextRecognize.TextRecognition(app_id = "2*****7",api_key = "*********************",\
                secret_key = "W**************************Ny")
            I2T.imageToText("temp2.png")
            self.Text = I2T.SplicingText()
            #self.paste_img(pic)
            self.send_msg_to_clip(win32clipboard.CF_UNICODETEXT,self.Text)
            os.remove('temp2.png')
            #关闭当前窗口
            self.top.destroy()
            
        self.canvas.bind('<B1-Motion>', onLeftButtonMove) # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp) # 抬起左键
        #让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    """将图片保存入剪贴板"""
    def send_msg_to_clip(self,type_data, msg):
        """
        操作剪贴板分四步：
        1. 打开剪贴板：OpenClipboard()
        2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
        3. 往剪贴板写入数据：SetClipboardData()
        4. 关闭剪贴板：CloseClipboard()

        :param type_data: 数据的格式，
        unicode字符通常是传 win32con.CF_UNICODETEXT
        :param msg: 要写入剪贴板的数据
        """
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(type_data, msg)
        win32clipboard.CloseClipboard()

    
    def paste_img(self,image):
        """
        图片转换成二进制字符串，然后以位图的格式写入剪贴板

        主要思路是用Image模块打开图片，
        用BytesIO存储图片转换之后的二进制字符串

        :param file_img: 图片的路径
        """

        # 声明output字节对象
        output = BytesIO()

        # 用BMP (Bitmap) 格式存储
        # 这里是位图，然后用output字节对象来存储
        image.save(output, 'BMP')

        # BMP图片有14字节的header，需要额外去除
        data = output.getvalue()[14:]

        # 关闭
        output.close()

        # DIB: 设备无关位图(device-independent bitmap)，名如其意
        # BMP的图片有时也会以.DIB和.RLE作扩展名
        # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
        self.send_msg_to_clip(win32clipboard.CF_DIB, data)




root = tk.Tk()
root.title("ScreenShot")
root.geometry('500x500')
root.resizable(True,True)

text = tk.Text(root)
text.pack()

def screenShot():
    root.state('icon')
    time.sleep(0.2)
    im = ImageGrab.grab(None)
    im.save('temp.png')
    im.close()
    w=FreeScreenShot(root,'temp.png')
    button_screenShot.wait_window(w.top)
    root.state('normal')
    os.remove('temp.png')
    text.insert("end",w.Text)


button_screenShot = tk.Button(root,text='Shot',command = screenShot)
button_screenShot.place(relx=0.5, rely=0.75, relwidth=0.2, relheight=0.2)




try:
    root.mainloop()
except:
    root.destroy()