from django.shortcuts import render, HttpResponse,render_to_response,redirect
from hostmanager import models
import json
from django import forms
from django.forms import widgets
from django.forms import fields
from django.forms import models as form_model

# Create your views here.


class User(forms.Form):
    # 字段本身只能验证，内含插件生成html
    name = fields.CharField(
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        max_length=20,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '最小长度为6',
        }
    )
    pwd = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        error_messages={
            'required': '密码不能为空',
        }
    )

    ugrup = fields.ChoiceField(
        initial=1,
        choices=models.User.type_choices,
        widget=widgets.Select(attrs={'class': 'form-control'})

    )
    # print(models.User.type_choices)
    # a = form_model.ModelChoiceField(queryset=models.User.objects.ugrup)


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
    # 首页
    uid = request.session.get("id")
    name = request.session.get("name")
    data = models.Host.objects.all()

    return render(request, "index.html", {"host_list": data, "name": name, })


class Host(forms.Form):
    id = fields.IntegerField(
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        required=True,
    )
    name = fields.CharField(
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        error_messages={
            'required': '用户名不能为空',
        }
    )
    ip = fields.GenericIPAddressField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        error_messages={
            'required': 'IP不能为空',
        }
    )
    port = fields.IntegerField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        error_messages={
            'required': '端口不能为空',
        }
    )


def select_host(request):
    # 主机信息
    id = request.POST.get("id")
    data = models.User.objects.filter(id=id).first()
    data_all = models.Host.objects.all()
    return HttpResponse({"all": data_all, "my": data})


def add_user(request):
    # 添加用户
    if request.method == "GET":
        obj = User()
        return render(request, "adduser.html", {"obj": obj})
    else:
        obj = User(request.POST)
        ret = obj.is_valid()
        if ret:
            models.User.objects.create(**obj.cleaned_data)
            return HttpResponse("ok")
        else:
            return HttpResponse("err")


class Permission(forms.Form):
    # print(models.User.objects.all().values_list("id", "name"))
    user = fields.ChoiceField(
        initial=1,
        choices=models.User.objects.all().values_list("id", "name"),
        widget=widgets.Select(attrs={'class': 'form-control', "id": "u"}),
    )
    s1 = fields.ChoiceField(
        widget=widgets.SelectMultiple(attrs={'class': 'form-control', "id": "hosts"}),
    )
    s2 = fields.ChoiceField(
        required=True,
        widget=widgets.SelectMultiple(attrs={'class': 'form-control', "id": "all_hosts"}),
    )

    def __init__(self, *args, **kwargs):
        super(Permission, self).__init__(*args, **kwargs)
        self.fields["user"].choices = models.User.objects.all().values_list("id", "name")

def permission(request):
    if request.method == "GET":
        obj = Permission()
        data1 = models.User.objects.all()
        return render(request, "permission.html", {"user_list": data1, "obj": obj})
    else:
        print(request.POST)
        a = {'user': [1], 's1': [1]}
        obj = Permission(a)
        ret = obj.is_valid()
        if ret:
            print('ok')
        else:
            print(obj.errors)



def host_group(request):
    return render(request, "hostgroup.html")


def get_hosts(request):
    if request.method == "GET":
        a_hosts = []
        a = int(request.GET.get("uid"))
        # print(a, type(a))
        hosts = list(models.User.objects.filter(id=a).first().h.all().values_list("id", "ip", "name"))
        all_host = list(models.Host.objects.all().values_list("id", "ip", "name"))
        for i in all_host:
            if i not in hosts:
                a_hosts.append(i)
        # print(hosts, a_hosts)
        return HttpResponse(json.dumps({"hosts": hosts, "all_hosts": a_hosts}))
    # else:
    #     print("eee")
    #     hosts = []  # 有权限的主机列表
    #     all_hosts = []  # 没有权限的主机列表
    #     uid = request.POST.get("uid")
    #     print(uid)
    #     data = models.User.objects.filter(id=uid).first().h.all()
    #     all_host = models.Host.objects.all()
    #     for i in data:
    #         temp = [i.id, i.ip, i.name]
    #         hosts.append(temp)
    #     for i in all_host:
    #         temp = [i.id, i.ip, i.name]
    #         if temp in hosts:
    #             continue
    #         all_hosts.append(temp)
    #
    #     return HttpResponse(json.dumps({"hosts": hosts, "all_hosts": all_hosts}))
    # return HttpResponse(data)


class Login(forms.Form):
    # 字段本身只能验证，内含插件生成html
    name = fields.CharField(
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        max_length=20,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '最小长度为6',
        }
    )
    pwd = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        error_messages={
            'required': '密码不能为空',
        }
    )


def login(request):
    # 登录
    if request.method == "GET":
        obj = Login()
        return render(request, 'login.html', {"obj": obj})
    else:
        obj = Login(request.POST)
        ret = obj.is_valid()  # 验证输入是否合格
        if ret:
            print(obj.cleaned_data)  # 打印用户输入数据
            data = models.User.objects.filter(**obj.cleaned_data).first()
            if data:
                request.session["auth"] = data.ugrup
                request.session["name"] = data.name
                request.session["id"] = data.id
                return redirect("/index")
            else:
                return render(request, 'login.html', {"obj": obj, "status": "用户名或密码错误"})
        else:
            print(obj.errors)
            return render(request, 'login.html', {"obj": obj})


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


class fm(forms.Form):
    user = forms.CharField()
    pwd = forms.CharField()
    email = forms.EmailField()


def test(request):
    if request.method == "GET":
        return render(request, "test.html")
    else:
        dd = request.POST.get("dd")
        print(dd, type(dd))
        a = json.loads(dd)
        print(a, type(a))
        return HttpResponse("ok")
