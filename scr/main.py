from flask import Flask, render_template
from settings import HOST, PORT, DEBUG

from mod_funcionario.funcionario import bp_funcionario
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
from mod_index.index import bp_index

app = Flask(__name__)

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

if __name__ == "__main__":

    app.run(host=HOST, port=PORT, debug=DEBUG)