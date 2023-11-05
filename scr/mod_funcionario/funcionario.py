from flask import Blueprint, render_template, request
import requests
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

# @bp_funcionario.route('/')
# def listaFuncionario():
#     return render_template('listaFuncionario.html'), 200

@bp_funcionario.route('/form')
def formFuncionario():
    return render_template('formFuncionario.html'), 200

@bp_funcionario.route('/', methods=['GET', 'POST'])
def listaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers = HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = request.form['senha']
        
        # monta o JSON para envio a API
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=HEADERS_API, json=payload)
        result = response.json()
        
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return listaFuncionario()
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])