import requests
from helpers.application import app
from helpers.database import db
from helpers.logging import logger
from models.UF import UF
from models.Mesorregiao import Mesorregiao


url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"

resposta = requests.get(url)
if resposta.status_code != 200:
    logger.error("Erro ao acessar a API do IBGE: %s", resposta.status_code)

todas_mesorregioes = resposta.json()

regioes_validas = {1, 2, 3, 4, 5}

with app.app_context():
    try:
        for meso in todas_mesorregioes:
            if meso["UF"]["regiao"]["id"] not in regioes_validas:
                continue
            co_mesorregiao = meso["id"]
            no_mesorregiao = meso["nome"]
            co_uf = meso["UF"]["id"]
            meso_existente = Mesorregiao.query.get(co_mesorregiao)
            if meso_existente:
                meso_existente.NO_MESORREGIAO = no_mesorregiao
                meso_existente.CO_UF = co_uf
            else:
                nova_meso = Mesorregiao(
                    CO_MESORREGIAO=co_mesorregiao,
                    NO_MESORREGIAO=no_mesorregiao,
                    CO_UF=co_uf
                )
                db.session.add(nova_meso)

        db.session.commit()
        print("A tabela Mesorregioes foi inserida/atualizada via SQLAlchemy com sucesso.")

    except Exception as e:
        db.session.rollback()
        logger.exception("Erro ao persistir mesorregiões com ORM")
        print(f"Erro detalhado: {e}")
