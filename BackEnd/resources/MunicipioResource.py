from flask import request, abort
from flask_restful import Resource, marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception
from models.Municipio import Municipio, MunicipioSchema, municipio_fields


class MunicipiosResource(Resource):
    def get(self):
        logger.info("GET ALL - Listagem de municípios")

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 1000))

        try:
            query = db.select(Municipio).order_by(Municipio.CO_MUNICIPIO)
            municipios = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()

            logger.info("Municípios retornados com sucesso")
            return marshal(municipios, municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar municípios")
            db.session.rollback()
            abort(500, description="Erro ao buscar municípios no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar municípios")
            abort(500, description="Erro interno inesperado.")

    def post(self):
        logger.info("POST - Novo município")
        schema = MunicipioSchema()
        dados = request.get_json()

        try:
            validado = schema.load(dados)
            novo_municipio = Municipio(**validado)
            db.session.add(novo_municipio)
            db.session.commit()
            return marshal(novo_municipio, municipio_fields), 201

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao inserir município")
            db.session.rollback()
            abort(500, description="Erro ao inserir município no banco.")
        except Exception:
            log_exception("Erro inesperado ao inserir município")
            abort(500, description="Erro interno inesperado.")


class MunicipioResource(Resource):
    def get(self, CO_MUNICIPIO):
        logger.info(f"GET BY CO_MUNICIPIO - Município {CO_MUNICIPIO}")
        try:
            municipio = db.session.get(Municipio, CO_MUNICIPIO)
            if not municipio:
                return {"erro": "Município não encontrado"}, 404
            return marshal(municipio, municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar município")
            abort(500, description="Erro ao buscar município no banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar município")
            abort(500, description="Erro interno inesperado.")

    def put(self, CO_MUNICIPIO):
        logger.info(f"PUT - Município {CO_MUNICIPIO}")
        schema = MunicipioSchema()
        dados = request.get_json()

        try:
            municipio = db.session.get(Municipio, CO_MUNICIPIO)
            if not municipio:
                return {"erro": "Município não encontrado"}, 404

            atualizados = schema.load(dados, partial=True)
            for campo, valor in atualizados.items():
                setattr(municipio, campo, valor)

            db.session.commit()
            return marshal(municipio, municipio_fields), 200

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao atualizar município")
            db.session.rollback()
            abort(500, description="Erro ao atualizar município.")
        except Exception:
            log_exception("Erro inesperado ao atualizar município")
            abort(500, description="Erro interno inesperado.")

    def delete(self, CO_MUNICIPIO):
        logger.info(f"DELETE - Município {CO_MUNICIPIO}")
        try:
            municipio = db.session.get(Municipio, CO_MUNICIPIO)
            if not municipio:
                return {"erro": "Município não encontrado"}, 404

            db.session.delete(municipio)
            db.session.commit()
            return {"mensagem": "Município removido com sucesso"}, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao remover município")
            db.session.rollback()
            abort(500, description="Erro ao remover município.")
        except Exception:
            log_exception("Erro inesperado ao remover município")
            abort(500, description="Erro interno inesperado.")
