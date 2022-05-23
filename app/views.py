import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET

from .models import *
from .forms import *
from django.http import JsonResponse
from django.db.models import Q


def def_content(request):
    content = {
        "active_users": Profile.objects.active_users,
        "popular_tags": Tag.objects.popular_tags,
        "this_user": Profile.objects.get_or_none(username=request.user.username)
    }

    return content


def question_paginator(request, count, src):
    paginator = Paginator(src, count)
    page = request.GET.get('page')
    additional = {
        'questions': paginator.get_page(page)
    }

    return additional


def answer_paginator(request, count, question_id):
    paginator = Paginator(Answer.objects.filter(question_id=question_id), count)
    page = request.GET.get('page')
    additional = {
        'question': Question.objects.get_or_none(id=question_id),
        'answers': paginator.get_page(page) if page != 'last' else paginator.get_page(paginator.num_pages)
    }

    return additional


def page_not_found_view(request, exception):
    content = def_content(request)

    return render(request, "404page.html", {"content": content}, status=404)


def index(request):
    content = def_content(request)
    content.update(question_paginator(request, 20, Question.objects.all()))

    return render(request, "index.html", {"content": content})


def question(request, question_id):
    content = def_content(request)
    content.update(answer_paginator(request, 5, question_id))

    if content['question'] is None:
        return render(request, "404page.html", {'content': def_content(request)})

    if request.method == 'GET':
        content['answer_form'] = AnswerForm()
    elif request.method == 'POST':
        content['answer_form'] = AnswerForm(request.POST)
        if content['answer_form'].is_valid():
            new_answer = Answer.objects.create(author=content['this_user'],
                                               text=content['answer_form'].cleaned_data['text'],
                                               question=content['question'])
            new_answer.save()
            return redirect(
                ('{}?page=last#' + str(new_answer.id)).format(
                    reverse('question', args=[content['question'].id])))

    return render(request, "question_page.html", {"content": content})


def latest(request):
    content = def_content(request)
    content.update(question_paginator(request, 20, Question.objects.latest_questions()[0:5]))

    return render(request, "latest.html", {"content": content})


def top(request):
    content = def_content(request)
    content.update(question_paginator(request, 20, Question.objects.top_questions()[0:5]))

    return render(request, "top.html", {"content": content})


def tag(request, tag_name: str):
    content = def_content(request)
    content.update(question_paginator(request, 8, Question.objects.filter(tags__name=tag_name)))
    content['tag'] = tag_name

    return render(request, "tag.html",
                  {"content": content})


@login_required
def ask(request):
    content = def_content(request)

    if request.method == 'GET':
        content['ask_form'] = AskForm()
    elif request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            new_question = Question.objects.create(title=form.cleaned_data['title'], text=form.cleaned_data['text'],
                                                   author=content['this_user'])
            new_question.save()
            tag_names = form.cleaned_data['tags'].split(",")
            for tag_name in tag_names:
                new_tag, created = Tag.objects.all().get_or_create(name=tag_name)
                new_question.tags.add(new_tag)
            new_question.save()

            return redirect(reverse("question", args=[new_question.id]))

        content['ask_form'] = form

    return render(request, "ask.html", {"content": content})


def profile(request, profile_name='None'):
    content = def_content(request)
    content['editable'] = False

    if profile_name == 'None':
        if content['this_user'] is not None:
            content['profile'] = content['this_user']
            content['editable'] = True
        else:
            return render(request, "404page.html", {'content': def_content(request)})
    else:
        content['profile'] = Profile.objects.get_or_none(username=profile_name)
        if content['profile'] is None:
            return render(request, "404page.html", {'content': content})
        if content['this_user'] is not None and content['this_user'].username == profile_name:
            content['editable'] = True
    return render(request, "profile.html", {'content': content})


@login_required
def settings(request):
    content = def_content(request)

    if request.method == 'GET':
        content['settings_form'] = SettingsForm(
            initial={'username': content['this_user'].username, 'email': content['this_user'].email})

    elif request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES,
                            initial={'username': content['this_user'].username, 'email': content['this_user'].email})
        if form.has_changed():
            if form.is_valid():
                changes = form.changed_data
                print(changes)
                if 'username' in changes:
                    print("Username changed")
                    if Profile.objects.filter(username=form.cleaned_data['username']).exists():
                        form.add_error('username', 'User already exists')
                    else:
                        content['this_user'].username = form.cleaned_data['username']
                        content['this_user'].save()
                if 'password' in changes:
                    print("password changed")
                    content['this_user'].set_password(form.cleaned_data['password'])
                    content['this_user'].save()
                if 'email' in changes:
                    print("email changed")
                    content['this_user'].email = form.cleaned_data['email']
                    content['this_user'].save()
                if 'avatar' in changes:
                    print("avatar changed")
                    content['this_user'].avatar = request.FILES['avatar']
                    content['this_user'].save()
                auth.logout(request)
                auth.login(request, content['this_user'])

                return redirect(reverse("profile", args=[content['this_user'].username]))

        content['settings_form'] = form
    return render(request, "settings.html", {"content": content})


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    content = def_content(request)

    if request.method == 'GET':
        content['login_form'] = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
            else:
                form.add_error("username", "Wrong username or password")
                content['login_form'] = form

    return render(request, "login.html", {"content": content})


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    content = def_content(request)

    if request.method == 'GET':
        content['register_form'] = RegisterForm()
    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile, is_created = Profile.objects.get_or_create(username=form.cleaned_data['username'],
                                                                    email=form.cleaned_data['email'])
            if not is_created:
                form.add_error('username', "User already exists")
            else:
                new_profile.set_password(form.cleaned_data['password'])
                file = request.FILES.get('avatar', False)
                if file:
                    new_profile.avatar = file
                new_profile.save()
                auth.login(request, new_profile)

                return redirect(reverse('index'))

        content['register_form'] = form

    return render(request, "register.html", {"content": content})


# @login_required
@require_POST
def rate(request):
    data = json.loads(request.body)
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'code': 'FAIL'})

    if data.get('obj_name', False) == 'question':
        obj = Question.objects.get_or_none(id=data.get('obj_id', -1))
        if obj is None:
            return JsonResponse({'code': 'FAIL'})

    elif data.get('obj_name', False) == 'answer':
        obj = Answer.objects.get_or_none(id=data.get('obj_id', -1))
        if obj is None:
            return JsonResponse({'code': 'FAIL'})

    if data.get('action_name', False) == 'like':
        action = Rating.LIKE
    elif data.get('action_name', False) == 'dislike':
        action = Rating.DISLIKE
    else:
        return JsonResponse({'code': 'FAIL'})

    rating, created = Rating.objects.update_rating(obj, user, action)

    return JsonResponse(
        {'code': 'OK',
         'selection': rating.rating,
         'likes_count': obj.rating.get_likes().count(),
         'dislikes_count': obj.rating.get_dislikes().count()
         }
    )


# @login_required
@require_POST
def answer_correct(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'code': 'FAIL'})

    answer_id = request.POST.get('answer_id', -1)
    ans = Answer.objects.get_or_none(id=answer_id)

    if ans.author == user:
        ans.isCorrect = not ans.isCorrect
        ans.save()

    return JsonResponse({'cb_status': ans.isCorrect})


@require_GET
def search(request):
    content = def_content(request)
    search_request = request.GET.get('find', None)

    if search_request is None or search_request == '':
        return redirect(reverse("index"))

    result = Question.objects.all().filter(
        Q(text__icontains=search_request) | Q(title__icontains=search_request))

    content.update(question_paginator(request, 20, result))

    return render(request, "search.html", {'content': content})
