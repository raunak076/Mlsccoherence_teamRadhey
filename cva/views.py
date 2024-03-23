from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def index(request):
    print("hi")
    return render(request,'index.html')

def supportRender(request):
    return render(request,"VCAmodel.html")

@csrf_exempt
def processText(request):
    if request.method == "POST":
        print(request.body)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        email = data.get("text")
        print(email)
    response_data = {'message': 'Text received'}
    return JsonResponse(response_data)