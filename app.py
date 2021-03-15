import os
import sys
import click

from flask import Flask, render_template
from faker import Faker
from flask_sqlalchemy import SQLAlchemy


prefix = 'sqlite:///'

fake= Faker()
Faker.seed(0)


app = Flask(__name__)








@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    if len(movies)<20:
        for _ in range(5):
            movies.append({'title':fake.bs(), 'year':fake.year() })


    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
    

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))









@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404


    
@app.route('/')
def index():
   
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/', methods=['GET', 'POST'])