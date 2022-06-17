from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from funcy import join

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(requestform, selection):
    page = requestform.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    categories = [category.format() for category in selection]
    formatted_categories = categories[start:end]

    return formatted_categories


def create_app():
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.format() for category in categories]
        formatted_categories = join(formatted_categories)

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(Category.query.all())
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = paginate(request, questions)
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        if len(formatted_questions) == 0:
            abort(400)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(Question.query.all()),
            'categories': join(formatted_categories),
            'current_category': join(formatted_categories)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    # @cross_origin
    def delete_question(question_id):

        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            else:
                question.delete()
                questions = Question.query.order_by(Question.id).all()
                return jsonify({
                    'success': True,
                    'deleted': question_id,
                    'total_questions': len(Question.query.all())
                })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if (question is None or answer is None or category is None) and search is None:
                abort(422)
            elif search:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                formatted_questions = paginate(request, questions)

                return jsonify({
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(questions.all()),
                })
            else:
                question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                question.insert()
                return jsonify({
                    'success': True,
                    'created': question.id,
                })
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = paginate(request, questions)
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if len(formatted_questions) == 0 or category is None:
            abort(404)

        return jsonify({
            "success": True,
            'question': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category.format()
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()

        previous = body.get('previous_questions', None)
        category = body.get('quiz_category', 0)
        try:
            if category['id'] != 0:
                questions = Question.query.filter(Question.category == category['id']).all()
                question_list = []
                for question in questions:
                    question_list.append(question.id)

                question = random.choice(Question.query.filter(Question.category == category['id']).all())

                while question.id in previous:
                    question = random.choice(Question.query.filter(Question.category == category['id']).all())

                    if question_list.sort() == previous.sort():
                        return jsonify({
                            'success': True,
                            'question': None
                        })
            else:
                questions = Question.query.all()
                question_list = []
                for question in questions:
                    question_list.append(question.id)

                question = random.choice(Question.query.all())

                while question.id in previous:
                    question = random.choice(Question.query.all())

                    if question_list.sort() == previous.sort():
                        return jsonify({
                            'success': True,
                            'question': None
                        })

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    return app
