from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'troque-por-uma-chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Model
class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(500))

    def __repr__(self):
        return f'<Curso {self.nome}>'

# Form
class CursoForm(FlaskForm):
    nome = StringField('Qual é o nome do curso?', validators=[DataRequired()])
    descricao = TextAreaField('Descrição (250 caracteres)', validators=[DataRequired()])
    submit = SubmitField('Salvar')

# Rotas obrigatórias
@app.route('/')
def index():
    # Nome e prontuário pedidos no enunciado
    aluno = "Soraya Gomes da Silva"
    prontuario = "PT3032515"
    # data/hora local (ISO ou formatada) - usamos datetime local
    now_local = datetime.now()
    return render_template('index.html',
                           aluno=aluno,
                           prontuario=prontuario,
                           now_local=now_local)

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    form = CursoForm()
    if form.validate_on_submit():
        novo = Curso(nome=form.nome.data, descricao=form.descricao.data)
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('cursos'))
    cursos = Curso.query.all()
    return render_template('cursos.html', form=form, cursos=cursos)

# Rotas mínimas para módulos não desenvolvidos (mostram "Não disponível")
@app.route('/professores')
@app.route('/disciplinas')
@app.route('/alunos')
@app.route('/ocorrencias')
def nao_disponivel():
    return render_template('nao_disponivel.html'), 200

# Cria o DB se não existir
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
