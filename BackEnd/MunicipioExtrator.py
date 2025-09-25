# MunicipioExtrator.py

import requests
from helpers.application import app
from helpers.database import db
from helpers.logging import logger
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

resposta = requests.get(URL)
if resposta.status_code != 200:
    logger.error("Erro ao acessar a API do IBGE: %s", resposta.status_code)

todos_municipios = resposta.json()

with app.app_context():
    try:
        for municipio in todos_municipios:
            co_municipio = municipio.get("id")
            no_municipio = municipio.get("nome")
            microrregiao = municipio.get("microrregiao")
            co_microrregiao = microrregiao.get("id") if microrregiao else None
            municipio_existente = Municipio.query.get(co_municipio)
            if municipio_existente:
                municipio_existente.NO_MUNICIPIO = no_municipio
                municipio_existente.CO_MICRORREGIAO = co_microrregiao
            else:
                novo_municipio = Municipio(
                    CO_MUNICIPIO=co_municipio,
                    NO_MUNICIPIO=no_municipio,
                    CO_MICRORREGIAO=co_microrregiao
                )
                db.session.add(novo_municipio)

        db.session.commit()
        print("A tabela Municipios foi inserida/atualizada via SQLAlchemy com sucesso.")

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao persistir municipios com ORM")
