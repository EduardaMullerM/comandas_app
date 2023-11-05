from flask import Blueprint, render_template, request
import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE


bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

# @bp_cliente.route('/')
# def listaCliente():
#     return render_template('listaCliente.html'), 200

@bp_cliente.route('/form')
def formCliente():
    return render_template('formCliente.html'), 200


@bp_cliente.route('/', methods=['GET', 'POST'])
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