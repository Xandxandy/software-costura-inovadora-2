import os
import sys

from flask import Flask, render_template, request, redirect, url_for

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from back.clientes import listar_clientes, adicionar_cliente

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")

        adicionar_cliente(nome, email, telefone)

        return redirect(url_for("inicio"))

    clientes_df = listar_clientes()
    clientes = clientes_df.to_dict(orient="records")

    return render_template("index.html", clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)