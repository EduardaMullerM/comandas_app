from flask import Blueprint, jsonify, redirect, render_template, request, url_for
import requests
from mod_login.login import validaSessao
from settings import HEADERS_API, ENDPOINT_PRODUTO
from mod_produto.GeraPdf import PDF
from flask import send_file


bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

@bp_produto.route('/form')
@validaSessao
def formProduto():
    return render_template('formProduto.html'), 200

@bp_produto.route('/', methods=['GET', 'POST'])
@validaSessao
def listaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers = HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaProduto.html', result=result[0])
    except Exception as e:
        return render_template('listaProduto.html', msgErro=e.args[0])
    
@bp_produto.route('/edit', methods=['POST'])
@validaSessao
def edit():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        valor_unitario = request.form['valor_unitario']
        # monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'valor_unitario': valor_unitario}
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API, json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        return redirect(url_for('produto.listaProduto', msg=result[0]))
    except Exception as e:
        return render_template('listaProduto.html', msgErro=e.args[0])
    
@bp_produto.route("/form-edit-Produto", methods=['POST'])
@validaSessao
def formEditProduto():
    try:
        id_produto = request.form['id']
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        print(result[0])
        return render_template('formProduto.html', result=result[0])
    except Exception as e:
        return render_template('listaProduto.html', msgErro=e.args[0])
    
@bp_produto.route('/delete', methods=['POST'])
@validaSessao
def formDeleteProduto():
    try:
        # dados enviados via FORM
        id_produto = request.form['id_produto']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=HEADERS_API)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
        # return redirect(url_for('funcionario.listaFuncionario', msg=result[0]))
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        # return render_template('istaFuncionario.html', msgErro=e.args[0])
        return jsonify(erro=True, msgErro=e.args[0])

''' rotas para PDF '''
@bp_produto.route('/pdfTodos', methods=['POST'])
@validaSessao
def pdfTodos():
    geraPdf = PDF()
    geraPdf.listaTodos()
    return send_file('pdfProdutos.pdf')