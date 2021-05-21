import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


def cat_format(data):
    my_dict = {}
    for cat in data:
        my_dict[cat.id] = cat.type
    return (my_dict)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
  Endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def get_all_categories():

        if request.method != 'GET':
            abort(405)

        all_categories = Category.query.all()
        # if no categories are created, they must be added

        all_categories = cat_format(all_categories)

        return jsonify({
            'success': True,
            'categories': all_categories
        })

    @app.route('/questions', methods=['GET'])
    def get_all_questions():
        all_questions = Question.query.order_by('id').all()

        if len(all_questions) == 0:
            abort(404)

        current_questions = paginate_questions(request, all_questions)
        all_categories = Category.query.all()
        all_categories = cat_format(all_categories)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(all_questions),
            'categories': all_categories,
            'current_category': None
        })
    '''
  Handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.
  '''

    '''
  DELETE question using a question ID.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        removeQuestion = Question.query.filter(
            Question.id == question_id).one_or_none()
        if removeQuestion is None:
            abort(422)

        removeQuestion.delete()

        return jsonify({
            'success': True,
            'deleted_id': question_id,
        })

    '''
  Endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.
  '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        new_question = request.get_json()
        question = new_question.get('question')
        answer = new_question.get('answer')
        category = new_question.get('category')
        difficulty = new_question.get('difficulty')

        if question == '' or answer == '' or category == '' or difficulty == '':
            abort(400)

        create = Question(question=question, answer=answer,
                          category=category, difficulty=difficulty)

        create.insert()

        return jsonify({
            'success': True,
            'created': create.id
        })
    '''
  POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        if request.method != 'POST':
            abort(405)

        data = request.get_json()
        search = data.get('searchTerm')
        questions = Question.query.filter(
            Question.question.ilike(f'%{search}%')).all()
        questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': None
        })

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        questions_of_category = Question.query.filter(
            Question.category == category_id).all()

        if len(questions_of_category) == 0:
            abort(404)

        current = Category.query.get(category_id)
        questions_of_category = paginate_questions(
            request, questions_of_category)

        return jsonify({
            'success': True,
            'questions': questions_of_category,
            'total_questions': len(questions_of_category),
            'current_category': current.format()['type']
        })

    @app.route('/quizzes', methods=['POST'])
    def start_quizzes():
        info = request.get_json()

        previousQ = info.get('previous_questions')
        quizCat = info.get('quiz_category')

        if quizCat['id'] == 0:
            list = Question.query.filter(Question.id.notin_(previousQ)).all()
        else:
            list = Question.query.filter(
                Question.category == quizCat['id'], Question.id.notin_(
                    previousQ)).all()

        list = [listItem.format() for listItem in list]

        if len(list) == 0:
            sendQuestion = ''
        else:
            index = random.randint(0, len(list)-1)
            sendQuestion = list[index]

        return jsonify({
            'previousQuestions': previousQ,
            'question': sendQuestion,
        })

    '''
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
