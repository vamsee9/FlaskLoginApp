from operator import or_
from project.models import books
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


app = Flask(__name__)

app.config['SECRET_KEY'] = '9O4#$#%^)_$LWxN@#_+(*$j4K4igo$%&^#$rO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost:5432/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/search/<string:keyword>', methods=['GET','POST'])
def search(keyword):
    b = books.query.filter(or_(books.isbn==keyword, books.author==keyword, books.title==keyword, books.year==keyword))
    l = []
    for i in b:
        dic = {}
        dic["isbn"] = i.isbn
        dic["author"] = i.author
        dic["title"] = i.title
        dic["year"] = i.year
        l.append(dic)

    return jsonify({"books":l}), 200   
