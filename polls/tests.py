import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No polls are available.")
        self.assertQuerySetEqual(resp.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        past_q = create_question(question_text="Past question.", days=-30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_question_list"], [past_q])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        future_q = create_question(question_text="Future question", days=30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No polls are available.")
        self.assertQuerySetEqual(resp.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_q = create_question(question_text="Past question.", days=-30)
        future_q = create_question(question_text="Future question", days=30)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_question_list"], [past_q])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_q1 = create_question(question_text="Past question1.", days=-16)
        past_q2 = create_question(question_text="Past question2.", days=-3)
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerySetEqual(resp.context["latest_question_list"], [past_q1, past_q2])
