from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from mod_funcionario.GeraPdf import PDF
import requests
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO
from mod_login.login import validaSessao

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

# @bp_funcionario.route('/')
# def listaFuncionario():
#     return render_template('listaFuncionario.html'), 200

@bp_funcionario.route('/form')
@validaSessao
def formFuncionario():
    return render_template('formFuncionario.html'), 200

@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaSessao
def listaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers = HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/', methods=['POST'])
@validaSessao
def getFuncionarioByCPF():
    try:
        headers = HEADERS_API
        headers['cpf'] = request.form['cpf']
        headers['senha'] = request.form['senha']
        response = requests.get(ENDPOINT_FUNCIONARIO, headers = headers)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/insert', methods=['POST'])
@validaSessao
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
    
@bp_funcionario.route('/edit', methods=['POST'])
@validaSessao
def edit():
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
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo':
        grupo, 'senha': senha}
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API, json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('funcionario.listaFuncionario', msg=result[0]))
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
@validaSessao
def formEditFuncionario():
    try:
        id_funcionario = request.form['id']
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        print(result[0])
        return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('listaFuncionario.html', msgErro=e.args[0])
    
@bp_funcionario.route('/delete', methods=['POST'])
@validaSessao
def delete():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id_funcionario']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        # return redirect(url_for('funcionario.listaFuncionario', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        # return render_template('istaFuncionario.html', msgErro=e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])
    
''' rotas para PDF '''
@bp_funcionario.route('/pdfTodos', methods=['POST'])
@validaSessao
def pdfTodos():
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('pdfFuncionario.pdf')