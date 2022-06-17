# Udacitrivia


## About

Udacitrivia is a fullstack application based on Flask and React
the application does all of the following:

1. Displays questions - both all questions and by category. 
Questions will show the question, category and difficulty 
rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and 
answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or 
within a specific category.

## About the Stack

The application uses the Flask framework to host the backend 
and uses the React framework to handle the frontend. 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, 
pip and node installed on their local machines.


#### Backend
From the backend folder run `pip install requirements.txt`. 
All required packages are included in the requirements file. 

To run the application run the following commands: 
```
venv\Scripts\activate
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

These commands put the application in development and directs
our application to use the `__init__.py` file in our flaskr 
folder. Working in development mode shows an interactive 
debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default
and is a proxy in the frontend configuration. 

###### Database setup
With Postgres running, restore a database using the trivia.psql
file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Frontend

From the frontend folder, run the following commands to start 
the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as 
updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is
not hosted as a base URL. The backend API's are hosted at the
default, `http://127.0.0.1:5000/`, which is set as a proxy 
in the frontend configuration. 
- Authentication: This version of the application does not 
require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Not found
- 422: Not processable

### Endpoints 
#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the
ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An object with a single key, categories, that 
contains an object of id: category_string key:value pairs. 

```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of 
questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total 
questions, object including all categories, and current 
category string

```
{
    'success': True
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'current_category': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

#### GET '/categories/${id}/questions'
- Fetches questions for a category specified by id request
argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category,
total questions, and current category string 
```
{
    'question': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'total_questions': 100,
    'current_category': {
        '1': 'Science'
    }, 
}
```


#### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: A success value, the deleted question's id, a list
of all questions, omitting the deleted question.
```
{
    'success': True,
    'deleted': 1,
    'total_questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ]
}
```

#### POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body:
  ```
  {
  'previous_questions': [1, 4, 20, 15], 
  'quiz_category': {
      'id': 1,
      'type': 'Science'
  } 
  }
  ```
- Returns: a single new question object 

```
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
```

#### POST '/questions'
- Sends a post request in order to add a new question
- Request Body:
  ```
  {
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
  }
  ```
- Returns: A success value and the id of the newly created question
  ```
  {
     'success': True, 
     'created': 100
  }
  ```

#### POST '/questions'
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
  ```
  {
    'searchTerm': 'this is the term the user is looking for'
  }
  ```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'total_questions': 100,
    'current_category': 'Entertainment'
}
```