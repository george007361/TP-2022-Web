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
        "dislike_count": f"{int((i * i) / 2)}",
        "tags": ["Cars", "Help", "Homework"],
    } for i in range(1, 200)
]

ANSWERS = [
    {
        "id": i,
        "img_id": f"{i % 2 + 1}",
        "text": f"Answer #{i} Answer #{i} Answer #{i} Answer #{i} Answer #{i} ",
        "like_count": f"{int((i * i) / 3)}",
        "dislike_count": f"{int((i * i) / 4)}",
    } for i in range(1, 23)
]

ACTIVE = [
    {
     "name": "George",
    },
    {
        "name": "Andry",
    },
    {
        "name": "John",
    },
]

HOTTAGS = [
    {
        "name": "Summer",
        "level": 1,
    },
    {
        "name": "Winter",
        "level": 3,
    },
    {
        "name": "Computer",
        "level": 3,
    },

    {
        "name": "Cars",
        "level": 2,
    },

    {
        "name": "Session",
        "level": 1,
    },

    {
        "name": "VK",
        "level": 2,
    },
]

def index(request):
    paginator = Paginator(QUESTIONS, 20)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "index.html", {'active_users': ACTIVE, 'hot_tags': HOTTAGS, 'questions_list': content})


def ask(request):
    return render(request, "ask.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def settings(request):
    return render(request, "settings.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def question(request, i: int):
    paginator = Paginator(ANSWERS, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "question_page.html", {"question": QUESTIONS[i - 1], "answers_list":content, "active_users": ACTIVE, 'hot_tags': HOTTAGS})


def hot(request):
    paginator = Paginator(QUESTIONS, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "hot.html", {"questions_list": content, "active_users": ACTIVE, 'hot_tags': HOTTAGS})


def tag(request, i:str):
    paginator = Paginator(QUESTIONS, 8)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return render(request, "tag.html", {"tag": i, "questions_list": content, "active_users": ACTIVE, 'hot_tags': HOTTAGS})


def login(request):
    return render(request, "login.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def signup(request):
    return render(request, "register.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})
