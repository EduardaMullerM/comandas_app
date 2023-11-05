from flask import Blueprint, render_template
import requests
from settings import HEADERS_API, ENDPOINT_PRODUTO


bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

# @bp_produto.route('/')
# def listaProduto():
#     return render_template('listaProduto.html'), 200

@bp_produto.route('/form')
def formProduto():
    return render_template('formProduto.html'), 200

@bp_produto.route('/', methods=['GET', 'POST'])
def listaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers = HEADERS_API)
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result[0])
        return render_template('listaProduto.html', result=result[0])
    except Exception as e:
        return render_template('listaProduto.html', msgErro=e.args[0])