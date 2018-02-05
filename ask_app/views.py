from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ask_app.models import Question, Answer
from django.contrib import auth
from ask_app.forms import LoginForm, SignupForm, AskQuestion
from django.utils import timezone


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
    page = request.GET.get('page')

    try:
        new_questions = paginator.page(page)

    except PageNotAnInteger:
        new_questions = paginator.page(1)

    except EmptyPage:
        new_questions = paginator.page(paginator.num_pages)

    return new_questions

def question(request, question_id):
    try:
        ques = Question.objects.get_single(int(question_id))
    except Question.DoesNotExist:
        raise Http404()

    # if request.method == 'POST':
    #     form = (request.POST)

    return render(request, 'ask_app/question.html', {'question': ques})

def index(request):
    questions_query = Question.objects.list_new()

    questions = paginate(questions_query, request)
    return render(request, 'ask_app/index.html', {'questions': questions})

def hot(request):
    hot_list = Question.objects.list_hot();

    questions = paginate(hot_list, request)
    return render(request, 'ask_app/hot.html', {'questions':questions})

def ask(request):
    if request.method == 'POST':
        form = AskQuestion(request.POST)

        if form.is_valid():
            question = Question.objects.create(author=request.user,
                                               date=timezone.now(),
                                               title=request.POST['title'],
                                               text=request.POST['text'])
            question.save()
    else:
        form = AskQuestion()
    return render(request, 'ask_app/ask.html', {'form': form})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('hot')

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('hot')
    else:
        form = SignupForm()

    return render(request, 'ask_app/register.html', {
            'form': form,
        })

def login(request):
    redirect = request.GET.get('continue', 'hot')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()

    return render(request, 'ask_app/login.html', {
            'form': form,
        })

def logout(request):
    redirect = request.GET.get('continue', 'hot')
    auth.logout(request)
    return HttpResponseRedirect(redirect)
