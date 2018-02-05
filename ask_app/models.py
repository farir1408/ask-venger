from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.urlresolvers import reverse
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()

class QuestionQuerySet(models.QuerySet):

    # preloads answers
    def with_answers(self):
        res = self.prefetch_related('answer_set')
        res = self.prefetch_related('answer_set__author')
        res = self.prefetch_related('answer_set__author__profile')
        return res

    # loads number of answers
    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    def order_by_popularity(self):
        return self.order_by('-likes')

    def with_date_greater(self, date):
        return self.filter(date__gt=date)

class QuestionManager(models.Manager):
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author()

    def list_new(self):
        return self.order_by('-date')

    def list_hot(self):
        return self.order_by('-likes')

    def get_single(self, id):
        res = self.get_queryset()
        return res.with_answers().get(pk=id)

    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    # tags = models.ManyToManyField(tag)

    objects = QuestionManager()

    class Meta:
        ordering = ['-date']

    def get_url(self):
        return reverse('questions', kwargs={'id': self.id})

class QuestionLikeManager(models.Manager):
    # adds a condition: with question
    def has_question(self, question):
        return self.filter(question=question)

    def sum_for_question(self, question):
        return self.has_question(question).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(
            author=author,
            question=question,
            defaults={'value': value}
        )

        question.likes = self.sum_for_question(question)
        question.save()
        return new

class QuestionLike(models.Model):
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()

class AnswerQuerySet(models.QuerySet):
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    def with_question(self):
        return self.select_related('question')

    def order_by_popularity(self):
        return self.order_by('-likes')

    def with_date_greater(self, date):
        return self.filter(date__gt=date)

class AnswerManager(models.Manager):
    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res.with_author()

    def create(self, **kwargs):
        ans = super(AnswerManager, self).create(**kwargs);

        text = ans.text[:100]
        if len(ans.text) > 100:
            text += '...'

        return ans

    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset().order_by_popularity().with_date_greater(week_ago)

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    objects = AnswerManager()

    class Meta:
        ordering = ['-correct', '-date', '-likes']

class AnswerLikeManager(models.Manager):
    # adds a condition: with answer
    def has_answer(self, answer):
        return self.filter(answer=answer)

    def sum_for_answer(self, answer):
        return self.has_answer(answer).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, answer, value):
        obj, new = self.update_or_create(
            author=author,
            answer=answer,
            defaults={'value': value}
        )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new

class AnswerLike(models.Model):
    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()
