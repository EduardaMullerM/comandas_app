from flask import Flask, render_template, session
import os
from datetime import timedelta

from settings import HOST, PORT, DEBUG, SESSION_TIME

from mod_funcionario.funcionario import bp_funcionario
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
from mod_index.index import bp_index
from mod_login.login import bp_login

app = Flask(__name__)

app.secret_key = os.urandom(12).hex()

# método para renovar o tempo da sessão
@app.before_request
def before_request():
    session.permanent = True
    session['tempo'] = int(SESSION_TIME)
    app.permanent_session_lifetime = timedelta(minutes=session['tempo'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404

@app.errorhandler(500)
def error500(error):
    return render_template("page500.html", erroHttp=error)

app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_index)
app.register_blueprint(bp_login)

if __name__ == "__main__":

    app.run(host=HOST, port=PORT, debug=DEBUG)