import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_q = Question(pub_date=future_time)

        self.assertIs(future_q.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_q = Question(pub_date=old_time)

        self.assertIs(old_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59, milliseconds=59, microseconds=59)
        recent_q = Question(pub_date=recent_time)

        self.assertIs(recent_q.was_published_recently(), True)