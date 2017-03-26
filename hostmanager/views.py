from django.shortcuts import render, HttpResponse,render_to_response,redirect
from hostmanager import models
import json

# Create your views here.


def index(request):
    host_list = []
    data = models.Host.objects.all()
    print(data)
    for i in data:
        print(i.id, i.name, i.ip, i.port, i.user)
        host_list.append({"id": i.id, "name": i.name, "ip": i.ip, "port": i.port, "user": i.user})
    print(host_list)
    return render(request,'index.html', {"host_list": host_list})


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        print(request.POST.get("name"))
        print(request.POST.get("pwd"))
        return redirect('/index')


def add_host(request):
    server_name = request.POST.get("name")
    ip = request.POST.get("ip")
    port = request.POST.get("port")
    user = request.POST.get("user")
    print(server_name, ip, port, user)
    obj = models.Host(name=server_name,ip=ip,port=port,user=user)
    a = obj.save()
    print(a)
    return redirect("/index")


def host_info(request):
    data = models.Host.objects.filter(id=request.POST.get('id')).first()
    send_data = {"id": data.id, "name": data.name, "ip": data.ip, "port": data.port, "user": data.user}
    return HttpResponse(json.dumps(send_data))

