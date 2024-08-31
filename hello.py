import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Disciplinas(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    alunos = db.relationship('Alunos', backref='disciplinas', lazy='dynamic')

    def __repr__(self):
        return '<Disciplinas %r>' % self.name


class Alunos(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, index=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'))

    def __repr__(self):
        return '<Alunos %r>' % self.name


class NameForm(FlaskForm):
    name = StringField('Cadastre o novo Aluno:', validators=[DataRequired()])
    disciplina = SelectField('Disciplina associada:', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Alunos=Alunos, Disciplinas=Disciplinas)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = NameForm()

    form.disciplina.choices = [(d.id, d.name) for d in Disciplinas.query.all()]

    if form.validate_on_submit():
        #user = User.query.filter_by(username=form.name.data).first()
        #if user is None:
        aluno = Alunos(name=form.name.data, disciplina_id=form.disciplina.data)
        db.session.add(aluno)
        db.session.commit()
        #session['known'] = False
        #else:
        #session['known'] = True
        #session['name'] = form.name.data
        return redirect(url_for('index'))
    all_user = Alunos.query.all()
    return render_template('index.html', form=form, all_user = all_user)
    #name=session.get('name'),
    #known=session.get('known', False))