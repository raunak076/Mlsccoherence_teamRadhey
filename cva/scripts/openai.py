# import openai
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# api_key = "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"

# @csrf_exempt
# def chatbot(request):
#     chatbot_response = None
#     if api_key is not None and request.method == 'POST':
#         openai.api_key = api_key
#         user_input = request.POST.get('user_input')
#         prompt = user_input

#         response = openai.Completion.create(
#             engine='gpt-3.5-turbo',
#             prompt=prompt,
#             max_tokens=256,
#             temperature=0.5
#         )
#         print("response is::", response)
#     return render(request, 'openai.html', {})
