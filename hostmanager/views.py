from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        print(request.POST.get("name"))
        print(request.POST.get("pwd"))
        return render(request, 'index.html')

