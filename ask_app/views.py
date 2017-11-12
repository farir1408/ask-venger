from django.shortcuts import render
from django.http import HttpResponse


def base(request):
    return render(request, "base.html")

def index(request):
    context = {
        'questions': [
            {
                'text': 'Какого цвета кулер1?',
                'user': 'GayOrgiy',
                'theme': 'Research',
            },
            {
                'text': 'Какого цвета кулер2?',
                'user': 'GayOrgiy',
                'theme': 'Research',
            },
            {
                'text': 'Какого цвета кулер3?',
                'user': 'GayOrgiy',
                'theme': 'Research',
            },
        ]
    }
    return render(request, 'ask_app/index.html', context=context)


def question(request):
    import random
    context = {
        'answers': [
            {
                'text': 'Твоя мамка',
                'user': 'Олег Мягкий',
                'votes': random.randint(228, 1488),
                'correct': random.randint(0, 1)
            },
            {
                'text': 'Твоя мамка',
                'user': 'Олег Мягкий',
                'votes': random.randint(228, 1488),
                'correct': random.randint(0, 1)
            },
            {
                'text': 'Твоя мамка',
                'user': 'Олег Мягкий',
                'votes': random.randint(228, 1488),
                'correct': random.randint(0, 1)
            }
        ]
    }
    return render(request, 'ask_app/question.html', context=context)

def ask(request):
    return render(request, 'ask_app/ask.html')

def login(request):
    return render(request, 'ask_app/login.html')

def register(request):
    return render(request, 'ask_app/register.html')
