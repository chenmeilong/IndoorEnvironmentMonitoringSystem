import wx, wx.grid
import pymysql
import socket
import time
import threading
from  usemodel import getevr
from  pyrevit import  reflashrevit

mysqlhost = 'localhost'
mysqlport = 3306          # MySQL的默认端口
mysqluser = 'root'
mysqlpasswd = '123456'
mysqldb = 'alldata'
mysqltable='datatable'
startnum=0                     #开始按钮 值
pidqualbuf = [0, 1, 1, 1, 1]  # 节点空气质量等级缓存
value=[                           #  参数   依次为   温度   湿度   mq， 空气质量等级   时间，
    [ 0,0, 0, 0, '00:00'],
    [0, 0, 0, 0, '00:00'],
    [0, 0, 0, 0, '00:00'],
    [0, 0, 0, 0, '00:00'],
    [0, 0, 0, 0, '00:00']
]


bind_ip = "localhost"    # 监听可用的接口
bind_port = 8080                 # 非特权端口号都可以使用 5001-65535: BSD服务器(非特权)端口,用来给用户自定义端口.
receivedata="0"                                        #初始化 socket接收数据的字符串
# AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 服务器监听的ip和端口号
server.bind((bind_ip, bind_port))
print("Listening on %s:%d" % (bind_ip, bind_port))
server.listen(5)              # 最大连接数


#socket服务器函数
def storedata():
    global receivedata                            #字符串是全局变量   用 global 声明
    # 等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
    client, addr = server.accept()
    print("Acception connection from %s" % (addr[0]))
    client_handler = threading.Thread(target=handle_client, args=(client,))    #多线程
    client_handler.start()

    if len(receivedata) >10:    #判读数据接收缓存是否刷新  避免出现空数据
        datelist = receivedata.split(',')
        print(datelist)  # 分离字符串到列表
        dipid=int(datelist[0])               #节点号的字符串 转换成int类型
        temperature =int(datelist[2])
        humidity  =int(datelist[3])
        mq135=int(datelist[5])                  #  正常训练的模型###############################################
        #mq135 = int(int(datelist[5])/100)       #用于10mq训练的模型
        quality = getevr(temperature, humidity, mq135)   #返回值为普通 int  表示空气质量等级 1-2-3-4级

        conn = pymysql.connect(host=mysqlhost,port=mysqlport,user=mysqluser,passwd=mysqlpasswd,db=mysqldb )
        cur = conn.cursor()
        sql_insert = "insert into "+mysqltable+" (dip,temp,humi,mq,qual,time) values('%d','%d','%d','%d','%d','%s')"
        cur.execute(sql_insert % (dipid, temperature, humidity, mq135, quality, time.strftime("%Y-%m-%d %H:%M:%S")))

        cur.close()
        conn.commit()
        conn.close()

    time.sleep(0.5)

# 客户处理线程   多线程服务函数
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(request)
    global receivedata
    receivedata = str(request, encoding = "utf-8")
    client_socket.close()


#表格操作类
class GridData(wx.grid.GridTableBase):
    _cols = "温度('C) 湿度(%RH) MQ-135 空气质量等级 时间".split()
    _rows = "节点1 节点2 节点3 节点4 平均".split()
    _data = value
    _highlighted = set()
    def GetColLabelValue(self, col):
        return self._cols[col]      #列的标签
    def GetRowLabelValue(self, col):
        return self._rows[col]      # 行的标签
    def GetNumberRows(self):
        return len(self._data)       #设置行数
    def GetNumberCols(self):
        return len(self._cols)        #设置列数
    def GetValue(self, row, col):
        return self._data[row][col]
    def SetValue(self, row, col, val):
        self._data[row][col] = val
    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)

class Test(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"数据显示窗口" , size = ( 350, 320))                     #窗口大小及标题
        self.icon = wx.Icon('hrbu.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)                               #设置窗口标题和ico图标

        self.data = GridData()                   #实例化 表格
        self.grid = wx.grid.Grid(self)       #画表  实例化  wxGrid  对象
        self.grid.SetTable(self.data)     #初始化数据

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)          #设置按钮
        btn1 = wx.Button(self, label="start")
        self.Bind(wx.EVT_BUTTON, self.OnClick)            #绑定点击事件

        self.sizer = wx.BoxSizer(wx.VERTICAL)          #垂直的
        self.sizer.Add(self.grid,1,wx.EXPAND)          #水平的
        self.sizer.Add(btn1,0,wx.EXPAND)              #底部扩展按钮的位置

        self.SetSizer(self.sizer)             #设置 画布  分布
        self.SetAutoLayout(1)           #自动布局  调整窗口大小
        self.sizer.Fit(self)
        self.Show()                      #显示出来


    def OnClick(self, event):                   #按钮点击事件
        def fun_timer():                     #刷新表格数据
            con = pymysql.connect(host=mysqlhost, port=mysqlport, user=mysqluser, passwd=mysqlpasswd, db=mysqldb)
            cursor = con.cursor()
            sql = "select * from "+mysqltable+" where dip='%d'  order by id  desc limit 1    "  # 选取 dip=3的  再按照 id 排序，取最后一条数据

            for i in range(1,5):                    #4个节点循环四次
                cursor.execute(sql % (i))  # 执行sql语句
                result = cursor.fetchall()  # 获取查询的所有记录
                for var in result:  # row是一个元组
                    newvalue = list(var)           # # 除了时间  导出后全是int类型
                for j in range(1, 6):             #j  即代表一行
                    if j==5:
                        timestr=newvalue[j]
                        value[i-1][j-1]=timestr[11:19]
                    else:
                        value[i-1][j-1]=newvalue[j]
                    self.data.set_value(i - 1, j - 1, value[i - 1][j - 1])  # 表内数据修改  第一行数据
                pidqualbuf[i] = newvalue[4]                                          # 根据节点更新  空气质量数据  刷新到pyrevit
            averagetemp=int((value[0][0]+value[1][0]+value[2][0]+value[3][0]+0.5)/4)           #+0.5表示4四舍五入    计算传感器的平均值
            averagehumi=int((value[0][1]+value[1][1]+value[2][1]+value[3][1]+0.5)/4)
            averagemq135=int((value[1][2]+value[1][2]+value[2][2]+value[3][2]+0.5)/4)
            quality = getevr(averagetemp,averagehumi, averagemq135)  # 返回值为普通 int  表示空气质量等级 1-2-3-4级

            sql_insert = "insert into "+mysqltable+" (dip,temp,humi,mq,qual,time) values('%d','%d','%d','%d','%d','%s')"
            cursor.execute(sql_insert % (16, averagetemp, averagehumi, averagemq135, quality, time.strftime("%Y-%m-%d %H:%M:%S")))#存入16号节点  4位拨码开关最大支持0-15节点 避免与其他节点数据重复
            cursor.execute(sql % (16))  # 执行sql语句
            result = cursor.fetchall()  # 获取查询的所有记录
            for var in result:  # row是一个元组
                newvalue = list(var)  # # 除了时间  导出后全是int类型
            for j in range(1, 6):             #j  即代表一行
                if j==5:
                    timestr=newvalue[j]
                    value[4][j-1]=timestr[11:19]
                else:
                    value[4][j-1]=newvalue[j]
                self.data.set_value(4, j - 1, value[4][j - 1])  # 表内数据修改  第一行数据

            cursor.close()
            con.commit()                  #实物提交
            con.close()                   #关闭断开连接

            self.grid.Refresh()         #刷新数据到GUI界面中
            reflashrevit(pidqualbuf)            #刷新revit     需要从每个

            global timer
            timer = threading.Timer(10, fun_timer)       #隔5s刷新一次
            timer.start()

        global startnum
        if startnum==0:
            timer = threading.Timer(1, fun_timer)
            timer.start()#刷新数据   的进程
            startnum=startnum+1

def fun_timer():
    storedata()               # 数据处理后 储存数据到数据库
    global timer
    timer = threading.Timer(0.1, fun_timer)          #隔0.1s启动 一次fun_timer 函数
    timer.start()


timer = threading.Timer(1, fun_timer)              # 计时1s  进入执行 fun_timer函数
timer.start()

app = wx.App()                              #实例化一个app对象
app.TopWindow = Test()                         #实例化  一个  画窗口  的对象
app.TopWindow.Show()                          # 显示界面  窗口
app.MainLoop()                                 #进入这个死循环
