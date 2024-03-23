from django.shortcuts import render,HttpResponse

def index(request):
    print("hi")
    return render(request,'index.html')