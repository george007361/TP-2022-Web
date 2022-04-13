from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    help = 'Generator for database'

    def handle(self, *args, **options):
        params = {
            "USERS": options.get('users'),
            "QUESTIONS": options.get('questions'),
            "TAGS": options.get('tags'),
            "ANSWERS": options.get('answers'),
        }

        if options['default']:
            params["USERS"] = 100
            params["QUESTIONS"] = 800
            params["TAGS"] = 30
            params["ANSWERS"] = 2000

        print(params)
        self.create_profiles(params)
        self.create_tags(params)
        self.create_questions(params)
        self.create_answers(params)
        self.set_tags_to_questions(params)

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            action='store',
            default=0,
            help='Count of generated user profiles'
        )
        parser.add_argument(
            '-q',
            '--questions',
            action='store',
            default=0,
            help='Count of generated questions'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store',
            default=0,
            help='Count of generated tags'
        )
        parser.add_argument(
            '-a',
            '--answers',
            action='store',
            default=0,
            help='Count of generated answers'
        )
        parser.add_argument(
            '-d',
            '--default',
            action='store_true',
            default=True,
            help='Generate a lot of data'
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            default=True,
            help='Clear database'
        )

    def create_profiles(self, params):
        print('Creatings users...')
        for i in range(1, params["USERS"] + 1):
            new_us = django.contrib.auth.models.User(username=f'test_{i}')
            new_us.save()

        # Create
        print('Creating profiles...')
        profiles_to_cr = []
        for i in range(1, params["USERS"] + 1):
            profiles_to_cr.append(
                Profile(user=django.contrib.auth.models.User.objects.all().get(username=f'test_{i}'),
                        nickname=f'test_nick_{i}'))
        # Save
        Profile.objects.bulk_create(profiles_to_cr)

    def create_tags(self, params):
        print('Creatings tags...')
        tags_to_create = []
        for i in range(1, params["TAGS"] + 1):
            tags_to_create.append(Tag(name=f'testtag_{i}'))
        Tag.objects.bulk_create(tags_to_create)

    def create_questions(self, params):
        print('Creatings questions...')
        questions_to_create = []
        for i in range(1, params["QUESTIONS"] + 1):
            questions_to_create.append(Question(title=f'test_Q_{i}',
                                                text=f'test_text_{i}',
                                                author=Profile.objects.get(
                                                    nickname=f'test_nick_{max(i % params["USERS"], 1)}'),
                                                )
                                       )
        Question.objects.bulk_create(questions_to_create)

    def set_tags_to_questions(self, params):
        print('  Setting tags for questions...')
        questions_to_create = Question.objects.all()
        for i in range(1, params["QUESTIONS"] + 1):
            tag = Tag.objects.all().get(name=f'testtag_{i % params["TAGS"] if i % params["TAGS"] else params["TAGS"]}')
            questions_to_create[i - 1].tags.add(tag)
        Question.objects.bulk_create(questions_to_create)

    def create_answers(self, params):
        print('Creating answers...')
        count = 1000
        j = 0
        questions = Question.objects.all()
        while j < params["ANSWERS"] + 1:
            print(j, ' ', j + count)
            answers_to_create = []
            for i in range(j, j + count):
                answers_to_create.append(
                    Answer(
                        question=questions[
                            (i % params["QUESTIONS"] if i % params["QUESTIONS"] else params["QUESTIONS"]) - 1],
                        author=Profile.objects.get(
                            nickname=f'test_nick_{i % params["USERS"] if i % params["USERS"] else params["USERS"]}'),
                        text=f'Test answer {i}')
                )
            Answer.objects.bulk_create(answers_to_create)
            j += count
