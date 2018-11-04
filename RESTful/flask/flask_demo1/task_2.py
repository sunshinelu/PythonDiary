# -*- coding: utf-8 -*-

"""
参考链接：
http://www.pythondoc.com/flask-restful/first.html

测试方法：
在postman中使用get方法，输入如下链接：
http://localhost:5000/todo/api/v1.0/tasks

http://localhost:5000/todo/api/v1.0/tasks/2

http://localhost:5000/todo/api/v1.0/tasks/3


"""

from flask import Flask, jsonify
from flask import abort
from flask import make_response

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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)