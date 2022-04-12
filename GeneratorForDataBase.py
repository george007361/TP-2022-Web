import django.contrib.auth.models
from app.models import *


def create_profiles(params):
    print('Creatings users...')
    for i in range(1, params["PROFILES"] + 1):
        new_us = django.contrib.auth.models.User(username=f'test_{i}')
        new_us.save()

    # Create
    print('Creatings profiles...')
    profiles_to_cr = []
    for i in range(1, params["PROFILES"] + 1):
        profiles_to_cr.append(
            Profile(user=django.contrib.auth.models.User.objects.all().get(username=f'test_{i}'),
                    nickname=f'test_nick_{i}'))

    # Save
    Profile.objects.bulk_create(profiles_to_cr)


def create_tags(params):
    print('Creatings tags...')
    tags_to_create = []
    for i in range(1, params["TAGS"] + 1):
        tags_to_create.append(Tag(name=f'testtag_{i}'))
    Tag.objects.bulk_create(tags_to_create)


def create_questions(params):
    print('Creatings questions...')
    questions_to_create = []
    for i in range(1, params["QUESTIONS"] + 1):
        questions_to_create.append(Question(title=f'test_Q_{i}', text=f'test_text_{i}',
                                            author=Profile.objects.get(
                                                nickname=f'test_nick_{max(i % params["PROFILES"], 1)}'),
                                            ))
    Question.objects.bulk_create(questions_to_create)


def set_tags_to_questions(params):
    print('  Setting tags for questions...')
    questions_to_create = Question.objects.all()
    for i in range(1, params["QUESTIONS"] + 1):
        tag = Tag.objects.all().get(name=f'testtag_{i % params["TAGS"] if i % params["TAGS"] else params["TAGS"]}')
        questions_to_create[i - 1].tags.add(tag)
    Question.objects.bulk_create(questions_to_create)


def create_answers(params):
    print('Creating answers...')
    answers_to_create = []
    for i in range(1, params["ANSWERS"] + 1):
        question = Question.objects.get(title=f'test_Q_{i % params["QUESTIONS"] if i % params["QUESTIONS"] else params["QUESTIONS"] }')
        answers_to_create.append(
            Answer(
                question=question,
                author=Profile.objects.get(
                    nickname=f'test_nick_{i % params["PROFILES"] if i % params["PROFILES"] else params["PROFILES"]}'),
                text=f'Test answer {i}')
        )

    Answer.objects.bulk_create(answers_to_create)


PARAMS = {
    "PROFILES": 10,
    "QUESTIONS": 500,
    "TAGS": 100,
    "ANSWERS": 1500,
}

create_profiles(PARAMS)
create_tags(PARAMS)
create_questions(PARAMS)
create_answers(PARAMS)
set_tags_to_questions(PARAMS)
