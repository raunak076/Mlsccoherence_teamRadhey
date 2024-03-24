# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json, requests
from django.contrib.auth.forms import UserCreationForm
from .models import User
import pickle
import numpy as np
from django.contrib.auth import authenticate, login
import random
import joblib
import json
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

# from transformers import BartForConditionalGeneration, BartTokenizer,BartForConditionalGeneration

# #! model below
# model = BartForConditionalGeneration.from_pretrained("SantiagoPG/chatbot_customer_service", forced_bos_token_id=0)
# #! tokenizer below
# tok = BartTokenizer.from_pretrained("facebook/bart-large")

with open('cva\intents.json', 'r') as file:
    intents = json.load(file)['intents']
# Initialize the lemmatizer and tokenizer
lemmatizer = WordNetLemmatizer()
tokenizer = word_tokenize
# Create a list of all words in the intents, and a list of all intents
words = []
classes = []
documents = []
for intent in intents:
    for pattern in intent['patterns']:
        # Tokenize and lemmatize each word in the pattern
        words_in_pattern = tokenizer(pattern.lower())
        words_in_pattern = [lemmatizer.lemmatize(word) for word in words_in_pattern]
        # Add the words to the list of all words
        words.extend(words_in_pattern)
        # Add the pattern and intent to the list of all documents
        documents.append((words_in_pattern, intent['tag']))
        # Add the intent to the list of all intents
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
# Remove duplicates and sort the words and classes
words = sorted(list(set(words)))
classes = sorted(classes)
# Create training data as a bag of words
training_data = []
for document in documents:
    bag = []
    # Create a bag of words for each document
    for word in words:
        bag.append(1) if word in document[0] else bag.append(0)
    # Append the bag of words and the intent tag to the training data
    output_row = [0] * len(classes)
    output_row[classes.index(document[1])] = 1
    training_data.append([bag, output_row])
# Shuffle the training data and split it into input and output lists
random.shuffle(training_data)
training_data = np.array(training_data, dtype=object)
train_x = list(training_data[:, 0])
train_y = list(training_data[:, 1])

# Define the neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(train_y[0]), activation='softmax')
])
# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(np.array(train_x), np.array(train_y), epochs=250, batch_size=5)

def get_response(user_input):
    # pickled_model,pickle_tokenizer,pickle_lemmatizer = joblib.load('./model.joblib')

    # Create a list of all words in the intents, and a list of all intents
    # words = []
    # classes = []
    # documents = []
    # for intent in intents:
    #     for pattern in intent['patterns']:
    #         # Tokenize and lemmatize each word in the pattern
    #         words_in_pattern = pickle_tokenizer(pattern.lower())
    #         words_in_pattern = [pickle_lemmatizer.lemmatize(word) for word in words_in_pattern]
    #         # Add the words to the list of all words
    #         words.extend(words_in_pattern)
    #         # Add the pattern and intent to the list of all documents
    #         documents.append((words_in_pattern, intent['tag']))
    #         # Add the intent to the list of all intents
    #         if intent['tag'] not in classes:
    #             classes.append(intent['tag'])

    # Tokenize and lemmatize the user input
    words_in_input = tokenizer(user_input.lower())
    words_in_input = [lemmatizer.lemmatize(word) for word in words_in_input]

    # Create a bag of words for the user input
    bag = [0] * len(words)
    for word in words_in_input:
        for i, w in enumerate(words):
            if w == word:
                bag[i] = 1

    # Predict the intent of the user input using the trained model
    results = model.predict(np.array([bag]), verbose=0)[0]
    # Get the index of the highest probability result
    index = np.argmax(results)
    # Get the corresponding intent tag
    tag = classes[index]

    # If the probability of the predicted intent is below a certain threshold, return a default response
    if results[index] < 0.5:
        return "I'm sorry, I don't understand. Can you please rephrase?"

    print(tag)
    # Get a random response from the intent
    for intent in intents:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])

    return response


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


# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

@csrf_exempt
def processText(data):
    # if request.method == "POST":
    #     print(request.body)
    #     json_data = request.body.decode('utf-8')
    #     data = json.loads(json_data)
    #     query = data.get("text")
    #     print(query)
    try:
        #! santiago model
        # print(data)
        # encoded_query = tok.encode(data, return_tensors="pt")            
        # inputs = {"inputs": encoded_query}
        # generated_output = model.generate(**inputs)
        # decoded_text = tok.batch_decode(generated_output, skip_special_tokens=True)[0]
        

    # Main loop to get user input and generate responses
        print(data)
        user_input = data
        response = get_response(user_input)
        print("CVA::",response)

        # return JsonResponse({'message':decoded_text})
        return response
    except Exception as e:
        return JsonResponse({"Error":e})

def lobby(request):
    return render(request,"channelDemo.html")