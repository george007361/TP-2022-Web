import time

from django.core.management.base import BaseCommand
from django.core.cache import cache
from app.models import Profile, Tag, Question


class Command(BaseCommand):
    help = 'Cache filler: pop tags, active users'

    def handle(self, *args, **options):
        active_users = Profile.objects.active_users(10)
        cache.set("active_users", active_users, 300)

        popular_tags = Tag.objects.popular_tags(10)
        cache.set("popular_tags", popular_tags, 300)

        top_questions = Question.objects.top_questions()
        cache.set("top_questions", top_questions, 300)
