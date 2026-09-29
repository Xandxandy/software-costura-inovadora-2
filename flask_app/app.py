import os
import sys

from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from back.clientes import (
    listar_clientes,
    adicionar_cliente,
    editar_cliente,
    inativar_cliente,
    obter_cliente,
    listar_clientes_inativos,
    reativar_cliente
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")

        adicionar_cliente(nome, telefone, email)

        return redirect(url_for("inicio"))

    clientes_df = listar_clientes()
    clientes = clientes_df.to_dict(orient="records")

    return render_template("index.html", clientes=clientes)

@app.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar(id_cliente):

    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        editar_cliente(id_cliente, nome, telefone, email)

        return redirect(url_for("inicio"))

    cliente = obter_cliente(id_cliente)

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )

@app.route("/inativar/<int:id_cliente>", methods=["POST"])
def inativar(id_cliente):

    inativar_cliente(id_cliente)

    return redirect(url_for("inicio"))

@app.route("/clientes/inativos")
def clientes_inativos():
    clientes_df = listar_clientes_inativos()
    clientes = clientes_df.to_dict(orient="records")

    return render_template(
        "clientes_inativos.html",
        clientes=clientes
    )

@app.route("/reativar/<int:id_cliente>", methods=["POST"])
def reativar(id_cliente):
    reativar_cliente(id_cliente)

    return redirect(url_for("clientes_inativos"))

if __name__ == "__main__":
    app.run(debug=True)