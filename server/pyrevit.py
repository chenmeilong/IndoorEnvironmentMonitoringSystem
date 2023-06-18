import xlwt
import time
from pymouse import *
#传入参数依次为节点号和评价模型的空气质量
def reflashrevit (pidevr):
    for i in range(1, 5):
        if pidevr[i]==1:
            pidevr[i]=4
            continue
        if pidevr[i]==2:
            pidevr[i]=3
            continue
        if pidevr[i]==3:
            pidevr[i]=2
            continue
        if pidevr[i]==4:
            pidevr[i]=1
            continue
    mouse = PyMouse()                   #实例化对象
    workbook = xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('Sheel1')
    worksheet.write(0, 0, pidevr[1])                 #初始的节点1红色位置      1红 2橙 3黄 4绿
    worksheet.write(0, 1, pidevr[2])                 #初始的节点2橙色位置
    worksheet.write(0, 2, pidevr[3])                 #初始的节点3黄色位置
    worksheet.write(0, 3, pidevr[4])                 #初始的节点4绿色位置
    workbook.save(r"d:\app\REVIT2016\Revit 2016\databuff.xls")
    mousex, mousey =mouse.position()  # 返回鼠标的坐标
    mouse.click(768,432,1)               #点击一次        1536*864分辨率
   # mouse.click(768,432,1)               #点击一次        1536*864分辨率
    mouse.move(mousex, mousey)                          #–鼠标移动到坐标(x,y)

def main():
    time.sleep(5)
    reflashrevit([0,4,4,4,4])
    time.sleep(5)
    reflashrevit([0,4,3,4,4])
    time.sleep(5)
    reflashrevit([0,1,1,1,3])
    time.sleep(5)
    reflashrevit([0,4,1,2,3])
if __name__ == '__main__':
    main()
