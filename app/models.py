import django.contrib.auth.models
import uuid
from django.db import models
from django.db.models import Count


class QuestionManager(models.Manager):
    def latest_questions(self):
        return self.all().order_by('-id')[0:5]

    def top_questions(self):
        return self.all().order_by('-rating__likes')[0:5]


class UsersManager(models.Manager):
    def active_users(self):
        Profile.objects.all().annotate()
        return self.all().annotate(active=Count('answer')).order_by('-active')[:5]


class TagManager(models.Manager):
    def popular_tags(self):
        return self.all().annotate(popular=Count('tags')).order_by('-popular')[:5]


def question_directory_path(instance, filename):
    return 'question_image/{0}/{1}'.format(str(instance.u_id), filename)


def user_avatar_directory_path(instance, filename):
    return 'user_avatars/{0}/{1}'.format(str(instance.u_id), filename)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    author = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='answer')
    text = models.TextField()
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, related_name='answer')
    isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([str(self.id), self.text[:10]])


class Question(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(upload_to=question_directory_path)
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, related_name='question')
    tags = models.ManyToManyField('Tag', related_name='tags')

    objects = QuestionManager()

    def __str__(self):
        return ' '.join([str(self.id), self.title])


class Tag(models.Model):
    name = models.CharField(max_length=256)

    objects = TagManager()

    def __str__(self):
        return ' '.join([self.name])


class Profile(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    u_id = models.UUIDField(default=uuid.uuid4, editable=False)

    user = models.OneToOneField(django.contrib.auth.models.User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to=user_avatar_directory_path)

    objects = UsersManager()

    def __str__(self):
        return ' '.join([str(self.id), self.nickname])


class Rating(models.Model):
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ' '.join([str(self.likes), str(self.dislikes)])
