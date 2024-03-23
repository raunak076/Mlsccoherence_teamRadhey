from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests
# Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("SantiagoPG/chatbot_customer_service")
# model = AutoModelForSeq2SeqLM.from_pretrained("SantiagoPG/chatbot_customer_service")

from transformers import BartForConditionalGeneration, BartTokenizer,BartForConditionalGeneration

#! model below
model = BartForConditionalGeneration.from_pretrained("SantiagoPG/chatbot_customer_service", forced_bos_token_id=0)
#! tokenizer below
tok = BartTokenizer.from_pretrained("facebook/bart-large")

# API_URL = "https://api-inference.huggingface.co/models/SantiagoPG/chatbot_customer_service"
# headers = {"Authorization": "Bearer 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"}

def index(request):
    print("hi")
    return render(request,'index.html')

def supportRender(request):
    return render(request,"VCAmodel.html")

def login(request):
    return render(request,"login.html")

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@csrf_exempt
def processText(request):
    if request.method == "POST":
        print(request.body)
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        query = data.get("text")
        print(query)
        try:
            #!
            encoded_query = tok.encode(query, return_tensors="pt")            
            inputs = {"inputs": encoded_query}
            generated_output = model.generate(**inputs)
            decoded_text = tok.batch_decode(generated_output, skip_special_tokens=True)[0]
            # print(f"Generated Text: {decoded_text}")
            return JsonResponse({'message':"Kaise ho Roshan babua"})
            # return HttpResponse("hi")
        except Exception as e:
            return JsonResponse({"Error":e})
    else:
        return JsonResponse({'message':'Sorry I am unable to understand you'})
    return JsonResponse({'Message':'Hello'})

def lobby(request):
    return render(request,"channelDemo.html")