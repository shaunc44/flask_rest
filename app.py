#!flask/bin/python
from flask import Flask, abort, jsonify, make_response, request


# WE ARE NOT USING A DB IN APP
# Source: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


@app.route('/')
def index():
    return "This is a flask - rest test app"


# GET (READ) METHODS
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_one_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404) # Page not found
    else:
        return jsonify({'task': task[0]})


# POST (CREATE) METHODS
# To post via curl:
# curl -i -H "Content-Type: application/json" -X POST -d '{"title": "Read a book"}' http://localhost:5000/tasks
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400) # Bad request
    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201


# PUT (UPDATE) METHOD
# To update with curl:
# curl -i -H "Content-Type: application/json" -X PUT -d '{"done": true}' http://localhost:5000/tasks/2
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404) # Page not found
    if not request.json:
        abort(400) # Bad request
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400) # Bad request
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400) # Bad request
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400) # Bad request
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# DELETE METHOD
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Page Not Found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)



