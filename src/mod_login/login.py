from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from funcoes import Funcoes
from functools import wraps

from settings import ENDPOINT_AUTH, HEADERS_API

bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')

@bp_login.route("/", methods=['GET', 'POST'])
def login():
    return render_template("formLogin.html")
    
@bp_login.route('/login', methods=['POST'])
def validaLogin():
    headers = HEADERS_API
    headers['cpf'] = request.form['usuario']
    headers['senha'] = request.form['senha']
    response = requests.post(ENDPOINT_AUTH, headers=headers)
    session.clear()

    try:
        result = response.json()

        # Se o status code não for 2xx, considera como erro
        response.raise_for_status()

        session['login'] = result
        print("tchau")
        return redirect(url_for('index.formIndex'))

    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            return render_template('formLogin.html', msgErro=['Usuário não encontrado!'])
        elif response.status_code == 403:
            return render_template('formLogin.html', msgErro=['Credenciais Inválidas!'])
        else:
            return render_template('formLogin.html', msgErro=[f'Erro: {response.status_code}'])

    except Exception as e:
        return render_template('formLogin.html', msgErro=[f'Erro inesperado: {str(e)}'])

@bp_login.route("/logoff", methods=['GET'])
def logoff():
    # limpa um valor individual
    session.pop('login', None)
    # limpa toda sessão
    session.clear()
    # retorna para a tela de login
    return redirect(url_for('login.login'))

# valida se o usuário esta ativo na sessão
def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            # descarta os dados copiados da função original e retorna a tela de login
            return render_template('formLogin.html', msgErro=['Usuário não logado!', 'Realize o login para acessar a página.'])
        else:
            # retorna os dados copiados da função original
            return f(*args, **kwargs)
        # retorna o resultado do if acima
    return decorated_function