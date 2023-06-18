from django.shortcuts import render,HttpResponse,redirect
# from django.shortcuts import render_to_response
from webapp import models
import json
import pymysql
#用户登录视图函数
def login(request):
    global u,p
    error_msg=''
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        u=request.POST.get('user')
        p=request.POST.get('pwd')
        obj = models.UserInfo.objects.filter(username=u, password=p).first()
        if obj:
            return redirect('/index.html/')
        else:
            error_msg='用户名或密码错误'
            return render(request,'login.html',{'error_msg':error_msg})
    else:
        return redirect('/index.html/')
#用户注册视图函数
def add_user(request):
    error_msg2=''
    if request.method == 'GET':
        return render(request,'add_user.html')
    elif request.method == 'POST':
        u1 = request.POST.get('user')
        p1 = request.POST.get('pwd')
        p2=request.POST.get('pwd2')
        if u1=='' or p1=='' or p2 =='':
            error_msg2 = '账号或密码不能为空'
            return render(request, 'add_user.html', {'error_msg2': error_msg2})
        elif p1!=p2:
            error_msg2 = '两次密码不一致,请重新输入'
            return render(request, 'add_user.html', {'error_msg2': error_msg2})
        elif p1:
            models.UserInfo.objects.create(username=u1, password=p1)
            return redirect('/login/')

def user_info(request):
    if request.method=='GET':
        user_list = models.UserInfo.objects.filter(username=u, password=p)
        return render(request, 'user_info.html', {'user_list': user_list})
    else:
        user_list=models.UserInfo.objects.filter(username=u, password=p)
        return render(request, 'user_info.html',{'user_list':user_list})


def user_detail(request,nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    return render(request,'user_detail.html',{'obj': obj})


def user_edit(request,nid):
    if request.method=='GET':
        obj = models.UserInfo.objects.filter(id=nid).first()
        return render(request,'user_edit.html',{'obj': obj})
    elif request.method=='POST':
        nid = request.POST.get('id')
        u1 = request.POST.get('username')
        p1 = request.POST.get('password')
        models.UserInfo.objects.filter(id = nid).update(username=u1,password=p1)
        return redirect('/user_info/')


def user_del(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user_info/')

def index(request):
    return render(request,'index.html')
def show(request):
    tem=[]
    hum=[]
    tim=[]
    mq=[]
    qual=[]

    con = pymysql.connect(host="localhost", user="root",
                          password="123456", db='alldata', port=3306)
    # 使用cursor()方法获取操作游标
    cur = con.cursor()
    # 1.查询操作
    # 编写sql 查询语句  user1 对应我的表名
    # sql = "select * from datatable  where dip=1 "
    sql = "select * from datatable  where dip='%d'  order by id  desc limit 7 "  # 选取 dip=3的  再按照 id 排序，取最后一条数据
    cur.execute(sql % (16))  # 执行sql语句
    result = cur.fetchall()  # 获取查询的所有记录
    # 遍历结果
    value = []
    for var in result:  # row是一个元组
        newvalue = list(var)
        value.append(newvalue)
    print(value)  # 除了时间  导出后全是int类型
    #####反向迭代
    tem_list = list(reversed([i[1] for i in value]))
    hum_list = list(reversed([i[2] for i in value]))
    mq_list = list(reversed([i[3] for i in value]))
    qual_list = list(reversed([i[4] for i in value]))
    tim_list = list(reversed([i[5] for i in value]))
    for i in range(0, 7):
       if qual_list[i]==4:
           qual_list[i] = 1
           continue
       if qual_list[i]==3:
           qual_list[i] = 2
           continue
       if qual_list[i]==2:
           qual_list[i] =3
           continue
       if qual_list[i] == 1:
           qual_list[i] =4
           continue
    qual_lists = [i * 25 for i in qual_list]
    mq_lists = [i / 10 for i in mq_list]
    print(hum_list)
    ####去掉列表中的[,]
    for i5 in tem_list:
        tem = ",".join([str(i5) for i5 in tem_list])
    for i6 in hum_list:
        hum = ",".join([str(i6) for i6 in hum_list])
    for i7 in tim_list:
        tim = ",".join([str(i7) for i7 in tim_list])
    for i8 in mq_lists:
        mq = ",".join([str(i8) for i8 in mq_lists])
    for i9 in qual_lists:
        qual = ",".join([str(i9) for i9 in qual_lists])
    print(tem)
    print(hum)
    con.close()  # 关闭连接
    ret1 = {'tem': tem, 'hum': hum,'tim':tim,'mq':mq,'qual':qual}
    ret = json.dumps(ret1)
    return HttpResponse(json.dumps(ret))


