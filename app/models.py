from django.db import models
from colorfield.fields import ColorField
from django.utils.six import python_2_unicode_compatible
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

TIME_CHOICE = (
    ('1', "1 min"),
    ('2', "2 min"),
    ('5', "5 min"),
    ('10', "10 min"),
    ('20', "20 min")
)

CATEGORY_CHOICE = (
    ('International', "International"),
    ('Policy', "Policy"),
    ('Society', "Society"),
    ('Economy', "Economy"),
    ('Culture', "Culture"),
    ('Sport', "Sport"),
    ('Science', "Science"),
    ('Ecology', "Ecology"),
    ('Other', 'Other')
)

RESPONSE_CHOICE = (
    ('0', "NO"),
    ('1', "YES")
)

DECISION_CHOICE = (
    ('0', "NO"),
    ('1', "YES")
)

SECRET_QUESTION = (
    ("What is the name of my country ?", "What is the name of my country ?"),
    ("Who am i ?", "Who am i ?"),
    ("Love i Canadian ?", "Love i Canadian ?"),
    ("What is your first trip ?", "What is your first trip ?")
)


class Parameter(models.Model):
    user = models.OneToOneField(User)
    isCorrector = models.CharField(max_length=3, choices=DECISION_CHOICE)
    goodPoint = models.IntegerField(default=0)
    secretQuestion = models.CharField(max_length=300, choices=SECRET_QUESTION)
    secretResponse = models.CharField(max_length=300)


class Article(models.Model):

    title = models.CharField(max_length=200)
    hang = models.TextField()
    youtube = EmbedVideoField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICE)
    author = models.ForeignKey(User, null=True, blank=True)
    corrector = models.ForeignKey(User, null=True, blank=True, related_name='corrector')
    time = models.CharField(max_length=3, choices=TIME_CHOICE)
    haveImage = models.CharField(max_length=3, choices=DECISION_CHOICE)
    decision = models.CharField(max_length=3, choices=DECISION_CHOICE)
    text = models.TextField(null=True, blank=True)
    interest = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, null=True)
    idArticle = models.IntegerField(default=0)
    goodPoint = models.IntegerField(default=0)
    badPoint = models.IntegerField(default=0)
    machineGoodPoint = models.IntegerField(default=0)
    machineBadPoint = models.IntegerField(default=0)
    oldMachineGoodPoint = models.IntegerField(default=0)
    oldMachineBadPoint = models.IntegerField(default=0)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Component(models.Model):

    component = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.component


class Fact(models.Model):

    text = models.CharField(max_length=300, blank=False, null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    goodPoint = models.IntegerField(default=0)
    badPoint = models.IntegerField(default=0)
    isPublish = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Justification(models.Model):

    decision = models.CharField(max_length=200, choices=RESPONSE_CHOICE)
    text = models.TextField()
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.text


class ArticleLike(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class Follow(models.Model):
    user = models.ForeignKey(User)
    target = models.ForeignKey(User, related_name='target')


class ArticleReadAfter(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class ArticleInterrest(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class Commentary(models.Model):
    comment = models.TextField()
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.comment


class Point(models.Model):
    user = models.ForeignKey(User)
    justification = models.ForeignKey(Justification)


class HaveImageArticle(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class HaveAuthorArticle(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class AuthorRecognize(models.Model):
    user = models.ForeignKey(User)
    author = models.ForeignKey(User, related_name='author')


class ArticleToCorrect(models.Model):
    article = models.ForeignKey(Article)
