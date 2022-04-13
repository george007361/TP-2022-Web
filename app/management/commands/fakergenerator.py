import random

from django.core.management.base import BaseCommand
import faker.providers
from faker import Faker
from app.models import *


class Command(BaseCommand):
    help = 'Generator for database'

    def handle(self, *args, **options):
        params = {
            "USERS": int(options.get('users')),
            "QUESTIONS": int(options.get('questions')),
            "TAGS": int(options.get('tags')),
            "ANSWERS": int(options.get('answers')),
        }

        print(params)

        if options.get('default'):
            return

        fake = Faker(["en_US"])

        print('Creating users...')
        names = []
        for _ in range(params["USERS"]):
            names.append(fake.unique.name())
            new_user = django.contrib.auth.models.User(username=names[_])
            new_user.save()

        print('Creating profiles...')
        profiles = []
        for _ in range(params["USERS"]):
            profiles.append(Profile(nickname=names[_],
                                    user=django.contrib.auth.models.User.objects.all().get(
                                        username=names[_])
                                    )
                            )
        Profile.objects.bulk_create(profiles)

        print('Creating tags...')
        tags = []
        for _ in range(params["TAGS"]):
            tags.append(Tag(name=fake.unique.word()))
        Tag.objects.bulk_create(tags)

        print('Creating questions...')
        questions = []
        for _ in range(params["TAGS"]):
            questions.append(
                Question(
                    title=fake.text(max_nb_chars=30),
                    text=fake.text(max_nb_chars=100),
                    author=Profile.objects.all().get(nickname=random.choice(names))
                )
            )
        Question.objects.bulk_create(questions)

        print('Creating answers...')
        answers = []
        questions = Question.objects.all()
        profiles = Profile.objects.all()
        for _ in range(params["ANSWERS"]):
            answers.append(
                Answer(
                    question=random.choice(questions),
                    author=random.choice(profiles),
                    text=fake.text(max_nb_chars=200)
                )
            )
        Answer.objects.bulk_create(answers)

        print('Setting tags to questions...')
        questions = Question.objects.all()
        tags = Tag.objects.all()
        for i in range(len(questions)):
            new_tags = []
            for j in range(random.randrange(1, 4)):
                new_tags.append(random.choice(tags))
            questions[i].tags.set(new_tags)
        Question.objects.bulk_create(questions)

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            action='store',
            default=10,
            help='Count of generated user profiles'
        )
        parser.add_argument(
            '-q',
            '--questions',
            action='store',
            default=100,
            help='Count of generated questions'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store',
            default=30,
            help='Count of generated tags'
        )
        parser.add_argument(
            '-a',
            '--answers',
            action='store',
            default=400,
            help='Count of generated answers'
        )
        parser.add_argument(
            '-d',
            '--default',
            action='store_true',
            default=False,
            help='Show default values'
        )
