from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
# Create your views here.
# questions = []
# for i in range(1, 10):
#     questions.append( {
#         "title": f"title #{i}",
#         "text": f"Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} ",
#         # "img": f"/img/question-{i % 5}.jpg",
#     })

QUESTIONS = [
    {
        "id": i,
        "img_id": f"{i % 5 + 1}",
        "title": f"title #{i}",
        "text": f"Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} Text #{i} ",
        "answers_count": f"{2 * i}",
        "like_count": f"{(i * i)}",
    } for i in range(1, 200)
]

ANSWERS = [
    {
        "id": i,
        "img_id": f"{i % 2 + 1}",
        "text": f"Answer #{i} Answer #{i} Answer #{i} Answer #{i} Answer #{i} ",
        "like_count": f"{(i * i)}",
    } for i in range(1, 23)
]


def index(request):
    paginator = Paginator(QUESTIONS, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "index.html", {'questions_list': content})


def ask(request):
    return render(request, "ask.html")


def settings(request):
    return render(request, "settings.html")


def question(request, i: int):
    paginator = Paginator(ANSWERS, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "question_page.html", {"question": QUESTIONS[i - 1], "answers_list":content})


def hot(request):
    paginator = Paginator(QUESTIONS, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "hot.html", {"questions_list": content})


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "register.html")
