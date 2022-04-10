from django.db import models

# Create your models here.


class Answer(models.Model):
    text = models.TextField()
    image = models.ImageField()
    isCorrect = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='Answer_of')
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, related_name='Rating_of_answer')

    def __str__(self):
        return ' '.join([self.id, self.text[:10]])


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField()
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, related_name='Rating_of_question')
    tags = models.ManyToManyField('Tag', related_name='tags')

    def __str__(self):
        return ' '.join([self.id, self.title])


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return ' '.join([self.id, self.name])


class Profile(models.Model):
    nickname = models.CharField(max_length=256)
    avatar = models.ImageField()
    # login
    # email

    def __str__(self):
        return ' '.join([self.id, self.nickname])


class Rating(models.Model):
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()

    def __str__(self):
        return ' '.join([self.id, self.likes, self.dislikes])