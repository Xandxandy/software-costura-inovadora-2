import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask_app.app import app


def test_pagina_clientes_carrega():
    cliente = app.test_client()

    resposta = cliente.get("/")

    assert resposta.status_code == 200


def test_pagina_servicos_carrega():
    cliente = app.test_client()

    resposta = cliente.get("/servicos")

    assert resposta.status_code == 200


def test_pagina_pedidos_carrega():
    cliente = app.test_client()

    resposta = cliente.get("/pedidos")

    assert resposta.status_code == 200


def test_pagina_orcamentos_carrega():
    cliente = app.test_client()

    resposta = cliente.get("/orcamentos")

    assert resposta.status_code == 200

def test_cadastro_cliente(monkeypatch):
    dados_recebidos = {}

    def adicionar_cliente_falso(
        nome,
        telefone,
        email,
        cep,
        logradouro,
        numero,
        complemento,
        bairro,
        cidade,
        uf
    ):
        dados_recebidos["nome"] = nome
        dados_recebidos["telefone"] = telefone
        dados_recebidos["email"] = email

    monkeypatch.setattr(
        "flask_app.app.adicionar_cliente",
        adicionar_cliente_falso
    )

    cliente = app.test_client()

    resposta = cliente.post(
        "/",
        data={
            "nome": "Cliente Teste",
            "telefone": "11999999999",
            "email": "teste@email.com",
            "cep": "",
            "logradouro": "",
            "numero": "",
            "complemento": "",
            "bairro": "",
            "cidade": "",
            "uf": ""
        }
    )

    assert resposta.status_code == 302
    assert dados_recebidos["nome"] == "Cliente Teste"
    assert dados_recebidos["telefone"] == "11999999999"
    assert dados_recebidos["email"] == "teste@email.com"


def test_cadastro_servico(monkeypatch):
    dados_recebidos = {}

    def adicionar_servico_falso(nome_servico, preco_base):
        dados_recebidos["nome_servico"] = nome_servico
        dados_recebidos["preco_base"] = preco_base

    monkeypatch.setattr(
        "flask_app.app.adicionar_servico",
        adicionar_servico_falso
    )

    cliente = app.test_client()

    resposta = cliente.post(
        "/servicos",
        data={
            "nome_servico": "Barra de calça",
            "preco_base": "35.00"
        }
    )

    assert resposta.status_code == 302
    assert dados_recebidos["nome_servico"] == "Barra de calça"
    assert dados_recebidos["preco_base"] == "35.00"

def test_cadastro_pedido(monkeypatch):
    dados_recebidos = {}

    def adicionar_pedido_falso(
        valor_total,
        data_pedido,
        status,
        id_cliente,
        observacoes
    ):
        dados_recebidos["valor_total"] = valor_total
        dados_recebidos["data_pedido"] = data_pedido
        dados_recebidos["status"] = status
        dados_recebidos["id_cliente"] = id_cliente
        dados_recebidos["observacoes"] = observacoes

    monkeypatch.setattr(
        "flask_app.app.adicionar_pedido",
        adicionar_pedido_falso
    )

    cliente = app.test_client()

    resposta = cliente.post(
        "/pedidos",
        data={
            "valor_total": "120.00",
            "data_pedido": "2026-10-07",
            "status": "Pendente",
            "id_cliente": "1",
            "observacoes": "Pedido de teste"
        }
    )

    assert resposta.status_code == 302
    assert dados_recebidos["valor_total"] == "120.00"
    assert dados_recebidos["data_pedido"] == "2026-10-07"
    assert dados_recebidos["status"] == "Pendente"
    assert dados_recebidos["id_cliente"] == "1"
    assert dados_recebidos["observacoes"] == "Pedido de teste"


def test_cadastro_orcamento(monkeypatch):
    dados_recebidos = {}

    def adicionar_pedido_falso(
        valor_total,
        data_pedido,
        status,
        id_cliente,
        observacoes
    ):
        dados_recebidos["valor_total"] = valor_total
        dados_recebidos["data_pedido"] = data_pedido
        dados_recebidos["status"] = status
        dados_recebidos["id_cliente"] = id_cliente
        dados_recebidos["observacoes"] = observacoes

    monkeypatch.setattr(
        "flask_app.app.adicionar_pedido",
        adicionar_pedido_falso
    )

    cliente = app.test_client()

    resposta = cliente.post(
        "/orcamentos",
        data={
            "valor_total": "80.00",
            "data_pedido": "2026-10-07",
            "id_cliente": "1",
            "observacoes": "Orçamento de teste"
        }
    )

    assert resposta.status_code == 302
    assert dados_recebidos["valor_total"] == "80.00"
    assert dados_recebidos["data_pedido"] == "2026-10-07"
    assert dados_recebidos["status"] == "Orçamento"
    assert dados_recebidos["id_cliente"] == "1"
    assert dados_recebidos["observacoes"] == "Orçamento de teste"