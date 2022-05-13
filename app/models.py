import uuid
from django.db import models
from django.db.models import Count

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from askmeGeorge import settings
from django.core.exceptions import ObjectDoesNotExist


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
        return self.all().order_by('-likes')


class ProfileManager(UserManager):
    def active_users(self):
        Profile.objects.all().annotate()
        return self.all().annotate(active=Count('answer')).order_by('-active')[:5]

    def get_or_none(self, **kwargs):
        try:
            return self.all().get(**kwargs)
        except ObjectDoesNotExist:
            return None


class TagManager(models.Manager):
    def popular_tags(self):
        return self.all().annotate(popular=Count('tags')).order_by('-popular')[:5]


# class LikeManager(models.Manager):
#     def add_like(self):
#         """Лайкает `obj`.
#         """
#         obj_type = ContentType.objects.get_for_model(obj)
#         like, is_created = Like.objects.get_or_create(
#             content_type=obj_type, object_id=obj.id, user=user)
#         return like
#
#     def remove_like(obj, user):
#         """Удаляет лайк с `obj`.
#         """
#         obj_type = ContentType.objects.get_for_model(obj)
#         Like.objects.filter(
#             content_type=obj_type, object_id=obj.id, user=user
#         ).delete()


# paths

def question_directory_path(instance, filename):
    return 'question_image/{0}/{1}'.format(str(instance.u_id), filename)


def user_avatar_directory_path(instance, filename):
    return 'user_avatars/{0}/{1}'.format(str(instance.u_id), filename)


def default_question_image_path():
    return 'question_image/default/default_image.jpg'


def default_user_avatar_path():
    return 'user_avatars/default/default_avatar.jpg'


# Models
class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='answer')

    text = models.TextField()

    isCorrect = models.BooleanField(default=False)

    likes = GenericRelation('Like')
    dislikes = GenericRelation('Dislike')

    def __str__(self):
        return ' '.join([str(self.id), self.text[:10]])


class Question(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='question')
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='tags')

    likes = GenericRelation('Like')
    dislikes = GenericRelation('Dislike')

    objects = QuestionManager()

    def __str__(self):
        return ' '.join([str(self.id), self.title])


class Tag(models.Model):
    name = models.CharField(max_length=256)

    objects = TagManager()

    def __str__(self):
        return ' '.join([self.name])


class Profile(AbstractUser):
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, default=default_user_avatar_path)

    objects = ProfileManager()

    def __str__(self):
        return ' '.join([str(self.id), self.username])


class Like(models.Model):
    counter = models.PositiveIntegerField(default=0)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.PROTECT)
    content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return ' '.join(str(self.object_id), str(self.counter))


class Dislike(models.Model):
    counter = models.PositiveIntegerField(default=0)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dislikes', on_delete=models.PROTECT)
    content_type = models.OneToOneField(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return ' '.join(str(self.object_id), str(self.counter))
