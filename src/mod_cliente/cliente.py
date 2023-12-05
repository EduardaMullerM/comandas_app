from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
from mod_cliente.GeraPdf import PDF
import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE
from mod_login.login import validaSessao



bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

# @bp_cliente.route('/')
# def listaCliente():
#     return render_template('listaCliente.html'), 200

@bp_cliente.route('/form')
@validaSessao
def formCliente():
    return render_template('formCliente.html'), 200


@bp_cliente.route('/', methods=['GET', 'POST'])
@validaSessao
def listaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers = HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaCliente.html', result=result[0])
    except Exception as e:
        return render_template('listaCliente.html', msgErro=e.args[0])
        
@bp_cliente.route('/insert', methods=['POST'])
@validaSessao
def insert():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        senha = request.form['senha']
        compra_fiado = 0
        dia_fiado = ""
        
        # monta o JSON para envio a API
        payload = {'id': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'senha': senha, 'compra_fiado':compra_fiado, 'dia_fiado':dia_fiado}
        
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload)
        result = response.json()
        
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return listaCliente()
    except Exception as e:
        return render_template('listaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/edit', methods=['POST'])
@validaSessao
def edit():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        # compra_fiado = request.form['compra_fiado']
        # dia_fiado = request.form['compra_fiado']
        senha = request.form['senha']
        # monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'compra_fiado': 0, 'dia_fiado': 0,'senha': senha}
        # executa o verbo PUT da API e armazena seu retorno
        print(id_cliente)
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('cliente.listaCliente', msg=result[0]))
    except Exception as e:
        return render_template('formCliente.html', msgErro=e.args[0])
    
@bp_cliente.route("/form-edit-cliente", methods=['POST'])
@validaSessao
def formEditCliente():
    try:
        id_cliente = request.form['id']
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        print(result[0])
        return render_template('formCliente.html', result=result[0])
    except Exception as e:
        return render_template('listaCliente.html', msgErro=e.args[0])
    
    
@bp_cliente.route('/delete', methods=['POST'])
@validaSessao
def delete():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id_cliente']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        # return redirect(url_for('funcionario.listaFuncionario', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        # return render_template('istaFuncionario.html', msgErro=e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])
    
    ''' rotas para PDF '''
@bp_cliente.route('/pdfTodos', methods=['POST'])
@validaSessao
def pdfTodos():
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('pdfCliente.pdf')