from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *


def page_not_found_view(request, exception):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "404page.html", {"content": content}, status=404)


def index(request):
    paginator = Paginator(Question.objects.all(), 20)
    page = request.GET.get('page')
    content = {
        'questions': paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "index.html", {"content": content})


def question(request, i: int):
    paginator = Paginator(Answer.objects.filter(question_id=i), 5)
    page = request.GET.get('page')
    content = {
        "question": Question.objects.get(id=i),
        "answers": paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "question_page.html", {"content": content})


def latest(request):
    content = {
        'questions': Question.objects.latest_questions,
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "latest.html", {"content": content})


def top(request):
    content = {
        'questions': Question.objects.top_questions,
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "top.html", {"content": content})


def tag(request, i: str):
    paginator = Paginator(Question.objects.filter(tags__name=i), 8)
    page = request.GET.get('page')
    content = {
        'tag': i,
        'questions': paginator.get_page(page),
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
    }
    return render(request, "tag.html",
                  {"content": content})


def ask(request):
    return render(request, "ask.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def settings(request):
    return render(request, "settings.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def login(request):
    return render(request, "login.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})


def signup(request):
    return render(request, "register.html", {"active_users": ACTIVE, 'hot_tags': HOTTAGS})
