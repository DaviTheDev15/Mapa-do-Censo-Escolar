import requests
from flask import Flask
from helpers.application import app
from helpers.database import db
from helpers.logging import logger
from models.UF import UF

url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

resposta = requests.get(url)
if resposta.status_code != 200:
    logger.error("Erro ao acessar a API do IBGE: %s", resposta.status_code)

todas_UFs = resposta.json()

with app.app_context():
    try:
        for uf in todas_UFs:
            uf_existente = UF.query.get(uf["id"])
            if uf_existente:
                uf_existente.SG_UF = uf["sigla"]
                uf_existente.NO_UF = uf["nome"]
            else:
                nova_uf = UF(
                    CO_UF=uf["id"],
                    SG_UF=uf["sigla"],
                    NO_UF=uf["nome"]
                )
                db.session.add(nova_uf)

        db.session.commit()
        print("UFs inseridas/atualizadas com sucesso via SQLAlchemy.")
    except Exception:
        db.session.rollback()
        logger.exception("Erro ao inserir/atualizar UFs via ORM.")
