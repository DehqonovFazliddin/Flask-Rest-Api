from email.policy import default
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    num_of_book = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Book(name = {name}, author = {author}, cost = {cost}, number = {num_of_book})"


book_put_args = reqparse.RequestParser()
book_put_args.add_argument("name", type=str, help="Name of the book is required", required=True)
book_put_args.add_argument("author", type=str, help="Author of the book is required", required=True)
book_put_args.add_argument("cost", type=int, help="Cost of Book is required", required=True)
book_put_args.add_argument("num_of_book", type=int, help="Number of book is required", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("name", type=str, help="Name of the book is required")
book_update_args.add_argument("author", type=str, help="Author of the book is required")
book_update_args.add_argument("cost", type=int, help="Cost of Book is required")
book_update_args.add_argument("num_of_book", type=int, help="Number of Book is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'cost': fields.Integer,
    'num_of_book': fields.Integer,
}

class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, mesage="Book was not found")
        return result
    
    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, mesage="Book id is taken ...")
        book = BookModel(id=book_id, name=args['name'], author=args['author'], cost=args['cost'], num_of_book=args['num_of_book'])
        db.session.add(book)
        db.session.commit()
        return book
        
    @marshal_with(resource_fields)
    def patch(self, book_id):
        args = book_update_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Book didn't find")
        
        if args['name']:
            result.name = args['name']

        if args['author']:
            result.author = args['author']
        
        if args['cost']:
            result.cost = args['cost']

        if args['num_of_book']:
            result.num_of_book = args['num_of_book']

        db.session.add(result)
        db.session.commit()

        return result

    def delete(self, book_id):
        book = BookModel.query.filter_by(id=book_id).delete()
        if not book:
            abort(404, message="We have not like book")
        db.session.commit()
        return "", 204

api.add_resource(Book, "/book/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)