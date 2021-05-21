import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:student@{}/{}".format(
            'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What is read and black all over?',
            'answer': 'A Newspaper',
            'category': 5,
            'difficulty': 5
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_categories_methods(self):
        response = self.client().post('/categories')
        self.assertEqual(response.status_code, 405)

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

    def test_add_new_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_delete_question(self):
        allQuestions = Question.query.order_by(Question.id).all()
        removeQuestion = allQuestions[-1].format()['id']
        response = self.client().delete(f'/questions/{removeQuestion}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['deleted_id'])

    def test_question_search(self):
        response = self.client().post(
            '/questions/search', json={'searchTerm': 'What'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_question_by_category(self):
        category_id = random.randint(1, 6)
        response = self.client().get(f'/categories/{category_id}/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_question_by_wrong_category(self):
        category_id = random.randint(7, 19)
        response = self.client().get(f'/categories/{category_id}/questions')
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_quiz(self):
        response = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'type': '', 'id': 0}})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['previousQuestions'], [])
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
