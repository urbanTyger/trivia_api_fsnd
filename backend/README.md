# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## API Endpoints

All endpoints to support all the quiz functionality from the frontend.

### All categories
GET  `'/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: ***None***
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
#### Sample Response: 
```
{
   '1' : "Science",
   '2' : "Art",
   '3' : "Geography",
   '4' : "History",
   '5' : "Entertainment",
   '6' : "Sports"
}
```
### All questions
GET  `'/questions'`

- Fetches a dictionary of all questions
- Request Arguments: ***None***
#### Sample Response: 
```
 [{
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "id": 14, 
    "question": "In which royal palace would you find the Hall of Mirrors?"
}], 
  "success": true, 
  "total_questions": 29 # total questions in database
```
### Delete a question by id
DELETE  `'/questions/<int:question_id>'`

- Deletes a row from the database corresponding to the id
- Request Arguments: ***id of the question as an integer***

#### Sample Response: 
```
{
  "deleted_id": 23, # id of deleted question
  "success": true
}
```
### Add a question to the database
POST  `'/questions'`

- Add a question to the database
- Request Arguments: ***JSON*** in the below dict format
- If any value is blank, a *400* Error will be returned 
  ```
  {
    'question': <string>, 
    'answer': <string>,
    'category': <integer>,
    'difficulty': <integer>, 
  }
  ```
#### Sample Response: 
```
{
  "created": 23, # id of created question
  "success": true
}

```
### Search for a question
POST  `'/questions/search'`

- Goes through the database and does a fuzzy search for the term
- Request Arguments: ***JSON***
  ```
  {
      'searchTerm': <string>
  }
  ```
- Returns: All questions that match the searchTerm
#### Sample Response: 
```
{
   'success': True,
   'questions': questions, # list of questions matching search
   'total_questions': len(questions), # number of questions matching 
   'current_category': None
}

```
### All questions by category
GET  `'/categories/<int:category_id>/questions'`

- Fetches a dictionary of questions that match the category id
- Request Arguments: ***category id as integer***
- Invalid category number, or zero questions found will return an error of 404
#### Sample Response: 
```
{
  "current_category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}


```
### Quiz questions
POST  `'/quizzes'`

- Fetches all questions that match the category supplied. Based on th category, the questions will be randomized and not repeated. 
- Request Arguments: ***JSON***
  ```
  {
      'previous_questions': [], # array of question ids used
      'quiz_category': {id, type}, # from Category table
  }
  ```
- If a category id of 0 is provided, all questions can be used
#### Sample Response: 
```
{
   'previousQuestions': [],
   'question': {<formatted question from database>},
}

```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
