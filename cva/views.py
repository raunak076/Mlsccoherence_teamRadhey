from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate, login


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
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or some other page.
            print("Login completed")
            return redirect('/')  # Replace 'success_url_name' with the name of your success URL
        else:
            # Return an 'invalid login' error message.
            print(" not Login completed")
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        print("Login not completed")
        return render(request, 'login.html')
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('pass')
        email = request.POST.get('email')

        # Check if all required fields are provided
        if name and password and email:
            # Create a new user object
            new_user = User.objects.create(
                name=name,
                password=password,
                email=email
            )
            print("User registered successfully.")
            # Redirect the user to a different page upon successful registration # Assuming 'login' is the name of your login page URL pattern
        else:
            print("One or more required fields are missing.")

    # If the request method is not POST or if there are errors, render the registration form
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


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