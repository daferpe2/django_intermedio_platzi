import datetime
from http import client
from urllib import response

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

    def test_future_quesiton_and_past_question(self):
        """Even if both an past future question extist, 
            only past question are display
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        past_question = create_question(question_text='Past questions', days=-30)
        future_question = create_question(question_text='Future questions', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [past_question]
                                 )
    
    def test_two_past_questions(self):
        """The questions index page may display multiple questions.
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        past_question1 = create_question(question_text='Past questions1', days=-30)
        past_question2 = create_question(question_text='Past questions2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [past_question1, past_question2]
                                 )
        
    def test_two_future_questions(self):
        """the question index pague may displey multiple questions in future"""
        past_question = create_question(question_text='Past questions', days=30)
        future_question = create_question(question_text='Future questions', days=40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 []
                                 )
        
class QuestionDatailViewTest(TestCase):
    def test_future_question(self):
        """
        The datil view of a question with a pub_date in the future
        returns a 404 error not found
        """
        future_question = create_question(question_text='Future questions', days=30)
        url = reverse('polls:detail', args=(future_question.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the pass
        display the question's text
        """
        past_question = create_question(past_question='Past questions', days=-30)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)
            
        
        