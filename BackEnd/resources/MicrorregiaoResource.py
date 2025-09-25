from flask import request, abort
from flask_restful import Resource, marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from helpers.database import db
from helpers.logging import logger, log_exception
from models.Microrregiao import Microrregiao, MicrorregiaoSchema, microrregiao_fields


class MicrorregioesResource(Resource):
    def get(self):
        logger.info("GET ALL - Listagem de microrregiões")

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 100))

        try:
            query = db.select(Microrregiao).order_by(Microrregiao.CO_MICRORREGIAO)
            microrregioes = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()

            logger.info("Microrregiões retornadas com sucesso")
            return marshal(microrregioes, microrregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar microrregiões")
            db.session.rollback()
            abort(500, description="Erro ao buscar microrregiões no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar microrregiões")
            abort(500, description="Erro interno inesperado.")

    def post(self):
        logger.info("POST - Nova microrregião")
        schema = MicrorregiaoSchema()
        dados = request.get_json()

        try:
            validado = schema.load(dados)
            nova_micro = Microrregiao(**validado)
            db.session.add(nova_micro)
            db.session.commit()
            return marshal(nova_micro, microrregiao_fields), 201

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao inserir microrregião")
            db.session.rollback()
            abort(500, description="Erro ao inserir microrregião no banco.")
        except Exception:
            log_exception("Erro inesperado ao inserir microrregião")
            abort(500, description="Erro interno inesperado.")


class MicrorregiaoResource(Resource):
    def get(self, CO_MICRORREGIAO):
        logger.info(f"GET BY CO_MICRORREGIAO- Microrregião {CO_MICRORREGIAO}")
        try:
            microrregiao = db.session.get(Microrregiao, CO_MICRORREGIAO)
            if not microrregiao:
                return {"erro": "Microrregião não encontrada"}, 404
            return marshal(microrregiao, microrregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar microrregião")
            abort(500, description="Erro ao buscar microrregião no banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar microrregião")
            abort(500, description="Erro interno inesperado.")

    def put(self, CO_MICRORREGIAO):
        logger.info(f"PUT - Microrregião {CO_MICRORREGIAO}")
        schema = MicrorregiaoSchema()
        dados = request.get_json()

        try:
            microrregiao = db.session.get(Microrregiao, CO_MICRORREGIAO)
            if not microrregiao:
                return {"erro": "Microrregião não encontrada"}, 404

            atualizados = schema.load(dados, partial=True)
            for campo, valor in atualizados.items():
                setattr(microrregiao, campo, valor)

            db.session.commit()
            return marshal(microrregiao, microrregiao_fields), 200

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao atualizar microrregião")
            db.session.rollback()
            abort(500, description="Erro ao atualizar microrregião.")
        except Exception:
            log_exception("Erro inesperado ao atualizar microrregião")
            abort(500, description="Erro interno inesperado.")

    def delete(self, CO_MICRORREGIAO):
        logger.info(f"DELETE - Microrregião {CO_MICRORREGIAO}")
        try:
            microrregiao = db.session.get(Microrregiao, CO_MICRORREGIAO)
            if not microrregiao:
                return {"erro": "Microrregião não encontrada"}, 404

            db.session.delete(microrregiao)
            db.session.commit()
            return {"mensagem": "Microrregião removida com sucesso"}, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao remover microrregião")
            db.session.rollback()
            abort(500, description="Erro ao remover microrregião.")
        except Exception:
            log_exception("Erro inesperado ao remover microrregião")
            abort(500, description="Erro interno inesperado.")
