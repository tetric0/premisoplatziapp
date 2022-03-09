import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

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