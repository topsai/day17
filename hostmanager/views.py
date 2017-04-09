from django.shortcuts import render, HttpResponse,render_to_response,redirect
from hostmanager import models
import json

# Create your views here.


def lg(func):  # 验证用户登录装饰器
    def wrap(request, *args, **kwargs):
        # 如果未登陆，跳转到指定页面
        if not request.session.get("name"):
            # print("no login")
            return redirect('/login')
        return func(request, *args, **kwargs)
    return wrap


@lg
def index(request):
    uid = request.session.get("id")
    name = request.session.get("name")
    data = models.Host.objects.all()
    data1 = models.User.objects.all()
    return render(request, "index.html", {"host_list": data, "name": name, "user_list": data1})


def select_host(request):
    id = request.POST.get("id")
    data = models.User.objects.filter(id=id).first()
    data_all = models.Host.objects.all()
    return HttpResponse({"all": data_all, "my": data})


def add_user(request):
    if request.method == "GET":
        print("get")
    else:
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        utype = int(request.POST.get("type"))
        g = models.UserGroup.objects.filter(id=utype).first()
        print(name, pwd, type(utype), g)
        ret = models.User.objects.create(name=name, pwd=pwd, ugrup=g)
        print(ret)
        return HttpResponse("ok")


def login(request):
    # 登录
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        obj = models.User.objects.filter(name=name, pwd=pwd).first()
        if obj:
            # auth = obj.ugroup.id
            request.session["auth"] = obj.ugrup.id
            request.session["name"] = name
            request.session["id"] = obj.id
            return redirect("/index")
        else:
            return render(request, 'login.html', {"status": "用户名或密码错误"})


def add_host(request):
    server_name = request.POST.get("name")
    ip = request.POST.get("ip")
    port = request.POST.get("port")
    user = request.POST.get("user")
    print(server_name, ip, port, user)
    obj = models.Host(name=server_name, ip=ip, port=port, user=user)
    a = obj.save()
    print(a)
    return redirect("/index")


def host_info(request):
    data = models.Host.objects.filter(id=request.POST.get('id')).first()
    send_data = {"id": data.id, "name": data.name, "ip": data.ip, "port": data.port, "user": data.users}
    return HttpResponse(json.dumps(send_data))


def host_del(request):
    models.Host.objects.filter(id=request.POST.get('id')).first().delete()
    return HttpResponse(json.dumps({"status": "ok"}))


def host_edit(request):
    id = request.POST.get("id")
    name = request.POST.get("name")
    ip = request.POST.get("ip")
    port = request.POST.get("port")
    obj = models.Host.objects.filter(id=id).first()
    obj.name = name
    obj.ip = ip
    obj.port = port
    obj.save()
    return HttpResponse("ok")


def login_off(request):
    request.session.delete()
    return redirect("/login")
