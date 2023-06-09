from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import Authentication
import json

@csrf_exempt
def Register(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        firstname = form_data.get('firstname')
        lastname = form_data.get('lastname')
        email = form_data.get('email')
        password = form_data.get('password')
        hashed_password = make_password(password)
        user = Authentication(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        user.save()
        return JsonResponse({'message': 'User registration successful'})
    else:
        return JsonResponse({'message': 'User registration failed'})

@csrf_exempt
def Login(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        # print(form_data)
        email = form_data.get('email')
        user_password = form_data.get('password')
        user = Authentication.objects.get(email=email)
        if user:
            hashed_password = user.password
            # print('hashed_password', hashed_password, check_password(user_password, hashed_password))
            if check_password(user_password, hashed_password):
                return JsonResponse({'message': 'Login Successful'})
            else:
                return JsonResponse({'message': 'Incorrect Password!'})
        else:
            return JsonResponse({'message': 'Invalid User. Please provide a exisitng user email!'})