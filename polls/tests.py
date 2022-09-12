import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.
#modelos o vistas

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_questions(self):
        """ test_was_published_recently_with_future_questions returns False
        for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='quien es el mejor',pub_date=time)
        self.assertIs(future_question.was_published_recently(),False) # yo afirmo que el resultado es falso de acuerdo al valor


