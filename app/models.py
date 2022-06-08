import os
from django.db import models
from django.db.models import Count, Sum
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser, UserManager
from askmeGeorge import settings
from django.core.exceptions import ObjectDoesNotExist

from dateutil.relativedelta import relativedelta
from django.utils.timezone import now


# Managers


class QuestionManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.all().get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def latest_questions(self):
        return self.all().order_by('-date')

    def top_questions(self):
        questions = self.all()
        questions_with_rating = []
        for question in questions:
            rating = question.rating.get_rating()
            questions_with_rating.append({'question': question, 'rating': rating})
        question_with_rating_sorted = sorted(questions_with_rating, key=lambda x: x['rating'], reverse=True)
        list_of_q = []
        for i in range(0, len(question_with_rating_sorted)):
            item = question_with_rating_sorted[i]
            list_of_q.append(item['question'])

        return list_of_q


class AnswerManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.all().get(**kwargs)
        except ObjectDoesNotExist:
            return None


class ProfileManager(UserManager):
    def active_users(self, count):
        Profile.objects.all().annotate()
        # return self.all().annotate(active=Count('answer') + Count('question')).order_by('-active')[:count]
        return self.all().annotate(active=Count('answer') + Count('question')).order_by('-active')[:count]

    def get_or_none(self, **kwargs):
        try:
            return self.all().get(**kwargs)
        except ObjectDoesNotExist:
            return None


class TagManager(models.Manager):
    def popular_tags(self, count):
        return self.all().filter(tags__date__gte=now() - relativedelta(months=3)).annotate(popular=Count('tags')).order_by('-popular')[:count]
        # return self.all().annotate(popular=Count('tags')).order_by('-popular')[:count]


class RatingManager(models.Manager):

    def get_likes(self):
        return self.all().filter(rating__gt=0)

    def get_dislikes(self):
        return self.all().filter(rating__lt=0)

    def get_rating(self):
        return self.all().aggregate(Sum('rating')).get('rating__sum') or 0

    @staticmethod
    def update_rating(obj, user, rating_type):
        rating = None
        created = None
        try:
            rating = Rating.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                        user=user)
            created = False
            if rating.rating != rating_type:
                rating.rating = rating_type
            else:
                rating.rating = 0
            rating.save()
        except Rating.DoesNotExist:
            rating = Rating.objects.create(user=user, content_object=obj, rating=rating_type)
            created = True

        return rating, created


# paths

def question_image_path(instance, filename):
    return 'question_image/{0}/{1}'.format(str(instance.id), filename)


def user_avatar_path(instance, filename):
    fname = 'user_avatars/{0}/{1}'.format(str(instance.id) + '_' + str(instance.username), filename)
    fname_full = os.path.join(settings.MEDIA_ROOT, fname)
    if os.path.exists(fname_full):
        os.remove(fname_full)
    return fname


def question_image_default_path():
    return 'question_image/default/default_image.jpg'


def user_avatar_default_path():
    return 'user_avatars/default/default_avatar.jpg'


# Models
class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='answer')

    text = models.TextField()

    isCorrect = models.BooleanField(default=False)

    rating = GenericRelation('Rating')
    date = models.DateTimeField(auto_now_add=True, blank=True)

    objects = AnswerManager()

    def __str__(self):
        return ' '.join([str(self.id), self.text[:10]])


class Question(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='question')
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='tags')

    rating = GenericRelation('Rating')

    objects = QuestionManager()

    def __str__(self):
        return ' '.join([str(self.id), self.title])


class Tag(models.Model):
    name = models.CharField(max_length=256)

    objects = TagManager()

    def __str__(self):
        return ' '.join([self.name])


class Profile(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default=user_avatar_default_path)

    objects = ProfileManager()

    def __str__(self):
        return ' '.join([str(self.id), self.username])


class Rating(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Like'),
        (LIKE, 'Dislike')
    )

    rating = models.IntegerField(choices=VOTES)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = RatingManager()

    def __str__(self):
        return ' '.join([str(self.id), str(self.content_object.__str__()), str(self.rating)])
