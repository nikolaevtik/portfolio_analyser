from django.shortcuts import render

APP_NAME = 'training'

def lesson1(request):
    return render(request, f'{APP_NAME}/lesson_1.html')

def index(request):
    return render(request, f'{APP_NAME}/base.html')