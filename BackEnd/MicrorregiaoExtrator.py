import requests
from helpers.application import app
from helpers.database import db
from helpers.logging import logger
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"

resposta = requests.get(url)
if resposta.status_code != 200:
    logger.error("Erro ao acessar a API do IBGE: %s", resposta.status_code)

todas_microrregioes = resposta.json()
regioes_validas = {1, 2, 3, 4, 5}

with app.app_context():
    try:
        for micro in todas_microrregioes:
            if micro["mesorregiao"]["UF"]["regiao"]["id"] not in regioes_validas:
                continue

            co_micro = micro["id"]
            no_micro = micro["nome"]
            co_meso = micro["mesorregiao"]["id"]

            micro_existente = Microrregiao.query.get(co_micro)

            if micro_existente:
                micro_existente.NO_MICRORREGIAO = no_micro
                micro_existente.CO_MESORREGIAO = co_meso
            else:
                nova_micro = Microrregiao(
                    CO_MICRORREGIAO=co_micro,
                    NO_MICRORREGIAO=no_micro,
                    CO_MESORREGIAO=co_meso
                )
                db.session.add(nova_micro)

        db.session.commit()
        print("A tabela Microrregioes foi inserida/atualizada via SQLAlchemy com sucesso.")

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao persistir microrregiões com ORM")
