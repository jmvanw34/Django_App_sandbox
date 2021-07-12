from django.db import models
from django.utils import timezone


class Tags(models.Model):

    tag_content = models.CharField(max_length=60, blank=False, null=False, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.tag_content



class Quotes(models.Model):

    quote_author = models.CharField(max_length=100, default="", blank=False, null=False)
    quote_content = models.TextField(max_length=501, blank=False, null=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags, related_name='tags')
    objects = models.Manager()

    def __str__(self):
        return self.quote_author

## add many-to-many field to connect Quotes and Tags

class Question(models.Model):
    question_text = models.CharField(max_length=150)
    author_text = models.CharField(max_length=50, null=True)
#     http://127.0.0.1:8000/GifsQuestionMark/questions/?search=me

