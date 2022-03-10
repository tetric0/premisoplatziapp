import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given 'question_text', and published the given
    number of days offset to now (negative for questions published in the past,
    positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions_published_passed_24_hours(self):
        """was_published_recently returns False for questions whose pub_date more than the last 24 hours"""
        time = timezone.now() - datetime.timedelta(hours=25)
        past_question = Question(question_text="Question text", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
    
    def test_was_published_recently_with_questions_published_now(self):
        """was_published_recently returns True for questions whose pub_date is now"""
        time = timezone.now()
        past_question = Question(question_text="Question text", pub_date=time)
        self.assertIs(past_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no question exists, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

    def test_future_questions(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )
    
    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question('Past question', days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )
    
    def test_future_question_and_past_question(self):
        """
        Even if both, past and future questions, exist only past questions are displayed
        """
        past_question = create_question(question_text='Past question', days=-30)
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may diplay multiple questions
        """
        past_question_1 = create_question(question_text='Past question 1', days=-30)
        past_question_2 = create_question(question_text='Past question 2', days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question_2, past_question_1]
        )

    def test_two_future_question(self):
        """
        The questions index page must not display any future questions
        """
        future_question_1 = create_question(question_text='Future question 1', days=30)
        future_question_2 = create_question(question_text='Future question 2', days=40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The Detail View of a Question with a 'pub_date' in the future
        must return a 404 Error (Not Found)
        """
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The Detail View of a Question with a 'pub_date' in the past
        must display the Question Text
        """
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):

    def test_no_question(self):
        """
        The Results View of a Question that doesn't exist
        must return a 404 Error (Not Found)
        """
        url = reverse("polls:results", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        """
        The Result View of a Question with a 'pub_date' in the future
        must return a 404 Error (Not found)
        """
        future_question = create_question(question_text="Future Question", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The Result View of a Question with a 'pub_date' in the past
        must display the Question's text
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)