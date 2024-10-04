from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api,reqparse
from mongoengine import NotUniqueError

app = Flask(__name__)
api = Api(app)
db = MongoEngine(app)

app.config['MONGODB_SETTINGS']= {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin'
}

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('first_name',
                          type = str,
                          required =True,
                          help="This field cannot be blank")

_user_parser.add_argument('last_name',
                          type = str,
                          required =True,
                          help="This field cannot be blank")

_user_parser.add_argument('cpf',
                          type = str,
                          required =True,
                          help="This field cannot be blank")

_user_parser.add_argument('email',
                          type = str,
                          required =True,
                          help="This field cannot be blank")

_user_parser.add_argument('birth_date',
                          type = str,
                          required =True,
                          help="This field cannot be blank")


class UserModel(db.Document):
    cpf = db.StringField(required=True,unique=True)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50,required=True)
    email = db.EmailField(required=True)
    birth_date = db.DateTimeField(required=True)
    
def valida_cpf(cpf: str) -> bool:
    # Remove caracteres especiais
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    
    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    
    # Verifica se os dígitos calculados são iguais aos dígitos do CPF
    return cpf[-2:] == f"{digito1}{digito2}"

class Users(Resource):
    def get(self):
        return {'message':'user 1'}

class User(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if not valida_cpf(data['cpf']):
            return {'message': 'Invalid CPF'}, 400
        
        try:    
            UserModel(**data).save()
            return {'message': 'User created successfully'}, 201
        except NotUniqueError:
            return {'message':'CPF already exists in database'},400
    
    def get(self):
        return {'message', 'CPF'}
    
    

api.add_resource(Users, '/users')
api.add_resource(User,'/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
