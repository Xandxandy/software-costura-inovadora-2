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

from back.servicos import (
    listar_servicos,
    adicionar_servico,
    editar_servico,
    deletar_servico,
    obter_servico
)

from back.pedidos import (
    listar_pedidos,
    adicionar_pedido,
    editar_pedido,
    deletar_pedido,
    obter_pedido,
    listar_clientes_para_pedido
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

@app.route("/servicos", methods=["GET", "POST"])
def servicos():
    if request.method == "POST":
        nome_servico = request.form.get("nome_servico")
        preco_base = request.form.get("preco_base")

        adicionar_servico(nome_servico, preco_base)

        return redirect(url_for("servicos"))

    servicos_df = listar_servicos()
    servicos = servicos_df.to_dict(orient="records")

    return render_template(
        "servicos.html",
        servicos=servicos
    )

@app.route("/servicos/editar/<int:id_servico>", methods=["GET", "POST"])
def editar_servico_rota(id_servico):

    if request.method == "POST":
        nome_servico = request.form.get("nome_servico")
        preco_base = request.form.get("preco_base")

        editar_servico(id_servico, nome_servico, preco_base)

        return redirect(url_for("servicos"))

    servico = obter_servico(id_servico)

    return render_template(
        "editar_servico.html",
        servico=servico
    )

@app.route("/servicos/excluir/<int:id_servico>", methods=["POST"])
def excluir_servico(id_servico):

    deletar_servico(id_servico)

    return redirect(url_for("servicos"))

@app.route("/pedidos", methods=["GET", "POST"])
def pedidos():

    if request.method == "POST":
        valor_total = request.form.get("valor_total")
        data_pedido = request.form.get("data_pedido")
        status = request.form.get("status")
        id_cliente = request.form.get("id_cliente")
        observacoes = request.form.get("observacoes")

        adicionar_pedido(
            valor_total,
            data_pedido,
            status,
            id_cliente,
            observacoes
        )

        return redirect(url_for("pedidos"))

    pedidos_df = listar_pedidos()
    pedidos_lista = pedidos_df.to_dict(orient="records")

    clientes_df = listar_clientes_para_pedido()
    clientes = clientes_df.to_dict(orient="records")

    return render_template(
        "pedidos.html",
        pedidos=pedidos_lista,
        clientes=clientes
    )

@app.route("/pedidos/editar/<int:id_pedido>", methods=["GET", "POST"])
def editar_pedido_rota(id_pedido):

    if request.method == "POST":
        valor_total = request.form.get("valor_total")
        data_pedido = request.form.get("data_pedido")
        status = request.form.get("status")
        id_cliente = request.form.get("id_cliente")
        observacoes = request.form.get("observacoes")

        editar_pedido(
            id_pedido,
            valor_total,
            data_pedido,
            status,
            id_cliente,
            observacoes
        )

        return redirect(url_for("pedidos"))

    pedido = obter_pedido(id_pedido)

    clientes_df = listar_clientes_para_pedido()
    clientes = clientes_df.to_dict(orient="records")

    return render_template(
        "editar_pedido.html",
        pedido=pedido,
        clientes=clientes
    )

@app.route("/pedidos/excluir/<int:id_pedido>", methods=["POST"])
def excluir_pedido(id_pedido):
    deletar_pedido(id_pedido)
    return redirect(url_for("pedidos"))

if __name__ == "__main__":
    app.run(debug=True)