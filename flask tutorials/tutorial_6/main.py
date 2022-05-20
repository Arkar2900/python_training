from flask import Flask
from flask_restx import fields, Api, Resource


app = Flask(__name__)
api = Api(app)
model = api.model('Model', {
    'todo_id': fields.String(readonly=True),
    'task': fields.String(required=True)
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for model in self.todos:
            if model['todo_id'] == id:
                return model
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, id, data):
        model = data
        model['todo_id'] = id
        self.todos.append(model)
        return model

    def update(self, id, data):
        model = self.get(id)
        model.update(data)
        return model


DAO = TodoDAO()
DAO.create('111', {'task': 'Build an API'})


@api.route('/todo')
class Todo(Resource):

    @api.marshal_list_with(model)
    def get(self):
        '''List all tasks'''
        return DAO.todos


@api.route('/todo/<string:id>')
class Todo_1(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.marshal_with(model)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.expect(model)
    @api.marshal_with(model)
    def post(self, id):
        return DAO.create(id, api.payload)

    @api.expect(model)
    @api.marshal_with(model, code=201)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
