"""Módulo para operações CRUD de clientes no banco de dados.

Este arquivo contém funções para adicionar, editar, deletar e listar clientes.
"""

import os
import sqlite3
import pandas as pd


def get_db_path():
    """Retorna o caminho do arquivo do banco de dados."""
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "sqlite_db", "Sqlite3.db")


def adicionar_cliente(
    nome: str,
    telefone: str,
    email: str,
    cep: str = "",
    logradouro: str = "",
    numero: str = "",
    complemento: str = "",
    bairro: str = "",
    cidade: str = "",
    uf: str = ""
) -> bool:
    """Adiciona um novo cliente ao banco de dados."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO cliente (
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
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
            )
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"Erro ao adicionar cliente: {e}")
        return False


def listar_clientes() -> pd.DataFrame:
    """Retorna um DataFrame com todos os clientes ativos."""
    try:
        conn = sqlite3.connect(get_db_path())

        query = """
            SELECT *,
                CASE status
                    WHEN 1 THEN 'Ativo'
                    ELSE 'Inativo'
                END AS status_texto
            FROM cliente
            WHERE status = 1
            ORDER BY id_cliente
        """

        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return pd.DataFrame()


def editar_cliente(
    id_cliente: int,
    nome: str,
    telefone: str,
    email: str,
    cep: str = "",
    logradouro: str = "",
    numero: str = "",
    complemento: str = "",
    bairro: str = "",
    cidade: str = "",
    uf: str = ""
) -> bool:
    """Edita um cliente existente."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE cliente
            SET nome = ?,
                telefone = ?,
                email = ?,
                cep = ?,
                logradouro = ?,
                numero = ?,
                complemento = ?,
                bairro = ?,
                cidade = ?,
                uf = ?
            WHERE id_cliente = ?
            """,
            (
                nome,
                telefone,
                email,
                cep,
                logradouro,
                numero,
                complemento,
                bairro,
                cidade,
                uf,
                id_cliente
            )
        )

        conn.commit()
        alterado = cursor.rowcount > 0
        conn.close()

        return alterado

    except sqlite3.Error as e:
        print(f"Erro ao editar cliente: {e}")
        return False


def deletar_cliente(id_cliente: int) -> bool:
    """Deleta um cliente do banco de dados."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM cliente WHERE id_cliente = ?",
            (id_cliente,)
        )

        conn.commit()
        alterado = cursor.rowcount > 0
        conn.close()

        return alterado

    except sqlite3.Error as e:
        print(f"Erro ao deletar cliente: {e}")
        return False


def inativar_cliente(id_cliente: int) -> bool:
    """Inativa um cliente no banco de dados."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cliente SET status = 0 WHERE id_cliente = ?",
            (id_cliente,)
        )

        conn.commit()
        alterado = cursor.rowcount > 0
        conn.close()

        return alterado

    except sqlite3.Error as e:
        print(f"Erro ao inativar cliente: {e}")
        return False


def listar_clientes_inativos() -> pd.DataFrame:
    """Retorna um DataFrame com os clientes inativos."""
    try:
        conn = sqlite3.connect(get_db_path())

        query = """
            SELECT *,
                CASE status
                    WHEN 1 THEN 'Ativo'
                    ELSE 'Inativo'
                END AS status_texto
            FROM cliente
            WHERE status = 0
            ORDER BY id_cliente
        """

        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    except sqlite3.Error as e:
        print(f"Erro ao listar clientes inativos: {e}")
        return pd.DataFrame()


def reativar_cliente(id_cliente: int) -> bool:
    """Reativa um cliente inativo no banco de dados."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cliente SET status = 1 WHERE id_cliente = ?",
            (id_cliente,)
        )

        conn.commit()
        alterado = cursor.rowcount > 0
        conn.close()

        return alterado

    except sqlite3.Error as e:
        print(f"Erro ao reativar cliente: {e}")
        return False


def obter_cliente(id_cliente: int) -> dict:
    """Obtém os dados de um cliente específico."""
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM cliente WHERE id_cliente = ?",
            (id_cliente,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id_cliente": row["id_cliente"],
                "nome": row["nome"],
                "telefone": row["telefone"],
                "email": row["email"],
                "status": row["status"],
                "cep": row["cep"] or "",
                "logradouro": row["logradouro"] or "",
                "numero": row["numero"] or "",
                "complemento": row["complemento"] or "",
                "bairro": row["bairro"] or "",
                "cidade": row["cidade"] or "",
                "uf": row["uf"] or ""
            }

        return {}

    except sqlite3.Error as e:
        print(f"Erro ao obter cliente: {e}")
        return {}