from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests

API_URL = "https://api-inference.huggingface.co/models/SantiagoPG/chatbot_customer_service"
headers = {"Authorization": "Bearer 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"}

def index(request):
    print("hi")
    return render(request,'index.html')

def supportRender(request):
    return render(request,"VCAmodel.html")

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@csrf_exempt
def processText(request):
    # if request.method == "POST":
    #     print(request.body)
    #     json_data = request.body.decode('utf-8')
    #     data = json.loads(json_data)
    #     query = data.get("text")
    #     print(query)
        
    #     try:
    #         response = requests.post(API_URL, headers=headers, json={"inputs":query})
    #         output = response.json()
    #         return JsonResponse({'message':output})
    #     except Exception as e:
    #         return JsonResponse({"Message":"Sorry Unable to understand you"})
    # else:
    #     return JsonResponse({'message':'Sorry I am unable to understand you'})
    return JsonResponse({'Message':'Hello'})