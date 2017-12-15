from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def base(request):
    return render(request, "base.html")

@csrf_exempt
def params(request):

    result = ['<!DOCTYPE html>', '<html>', '<p>WSGI</p>']

    result.append('Post:')
    result.append('<form method="post">')
    result.append('<input type="text" name="test">')
    result.append('<input type="submit" value="Send">')
    result.append('</form>')

    if request.method == 'POST':
        result.append(request.POST.urlencode())

    if request.method == 'GET':
        if request.GET.urlencode() != '':
            result.append('Get data:')
            for key, value in request.GET.items():
                keyvalue = key + " = " + value
                result.append(keyvalue)

    return HttpResponse('<br>'.join(result).encode('u8'))

def paginate(object_list, request):
    num_on_page = 4
    paginator = Paginator(object_list, num_on_page)
    print(paginator.num_pages)
    page = request.GET.get('page')

    try:
        new_questions = paginator.page(page)

    except PageNotAnInteger:
        new_questions = paginator.page(1)

    except EmptyPage:
        new_questions = paginator.page(paginator.num_pages)

    return new_questions

def index(request):
    import random
    context = {'questions':[]}
    question = {
                'text': 'Какого цвета кулер',
                'user': 'GayOrgiy',
                'theme': 'Research',
            },

    for i in range(10):
        context['questions'].append(question)

    # print(context['questions'])

    questions = paginate(context['questions'], request)

    # print(context['questions'])

    return render(request, 'ask_app/index.html', {'questions':questions})


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
