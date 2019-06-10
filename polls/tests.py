import datetime, requests
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice

def create_question(question_text):
	"""
	Create a question with the given `question_text` and published the
	given number of `days` offset to now (negative for questions published
	in the past, positive for questions that have yet to be published).
	"""
	time = timezone.now()
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
	def test_valid_vote(self):
		print(Question.objects.all())
		'''q = Question.objects.get(pk=2)
		c1 = q.choice_set.get(id=1)
		num = c1.votes
		URL = 'http://localhost:8000/api/polls/questions/1/vote/'
		params = {'choice_id': '1'}
		r = requests.patch(url=URL, data=params)
		self.assertEqual(num+1, c1.votes)'''