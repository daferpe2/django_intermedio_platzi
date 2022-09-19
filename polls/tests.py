import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
    """
    create a question with the given 'question_text'
    and publis de given number of days offset now (negative for questions publish in the past,
    positive for questions that have yet to be published)
     """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """ If not cuestion exist, an appropiate message is display"""
        response = self.client.get(reverse('polls:index')) # equivalente ulr de template traer resultado de la funcoin index, url de index .
        #  reverse trae el resultado del resultado de la url self.cliend.get peticion a http tipo get sobre la url y guardarlo en response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No exite encuensta')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question(self):
        """
        Question with a pub_date in the future aren't displayed on the index page.
        """
        create_question('future questions', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No exite encuensta")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """
        question = create_question('past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


