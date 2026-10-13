from django.test import TestCase
from django.urls import reverse

from .models import QuizQuestion, QuizSong


class QuizTests(TestCase):
    def setUp(self):
        self.song = QuizSong.objects.create(number=1, title="Test Song")
        for number in range(1, 11):
            QuizQuestion.objects.create(
                song=self.song,
                order=number,
                question=f"Question {number}",
                option_a="A",
                option_b="B",
                option_c="C",
                option_d="D",
                correct_option="a",
            )

    def test_first_question_is_available(self):
        response = self.client.get(
            reverse("quiz_song", kwargs={"song_number": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question 1")

    def test_correct_answer_is_counted_immediately(self):
        response = self.client.post(
            reverse("quiz_song", kwargs={"song_number": 1}) + "?question=1",
            {"answer": "a"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Correct")
        self.assertContains(response, "1/10")

    def test_incorrect_answer_is_counted_immediately(self):
        response = self.client.post(
            reverse("quiz_song", kwargs={"song_number": 1}) + "?question=1",
            {"answer": "b"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incorrect")
        self.assertContains(response, "0/10")
