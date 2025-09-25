from flask import request, abort
from flask_restful import Resource, marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from helpers.database import db
from helpers.logging import logger, log_exception
from models.Mesorregiao import Mesorregiao, MesorregiaoSchema, mesorregiao_fields


class MesorregioesResource(Resource):
    def get(self):
        logger.info("GET ALL - Listagem de mesorregiões")

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))

        try:
            query = db.select(Mesorregiao).order_by(Mesorregiao.CO_MESORREGIAO)
            mesorregioes = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()

            logger.info("Mesorregiões retornadas com sucesso")
            return marshal(mesorregioes, mesorregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar mesorregiões")
            db.session.rollback()
            abort(500, description="Erro ao buscar mesorregiões no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar mesorregiões")
            abort(500, description="Erro interno inesperado.")

    def post(self):
        logger.info("POST - Nova mesorregião")
        schema = MesorregiaoSchema()
        dados = request.get_json()

        try:
            validado = schema.load(dados)
            nova_mesoreg = Mesorregiao(**validado)
            db.session.add(nova_mesoreg)
            db.session.commit()
            return marshal(nova_mesoreg, mesorregiao_fields), 201

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao inserir mesorregião")
            db.session.rollback()
            abort(500, description="Erro ao inserir mesorregião no banco.")
        except Exception:
            log_exception("Erro inesperado ao inserir mesorregião")
            abort(500, description="Erro interno inesperado.")


class MesorregiaoResource(Resource):
    def get(self, CO_MESORREGIAO):
        logger.info(f"GET BY CO_MESORREGIAO - Mesorregião {CO_MESORREGIAO}")
        try:
            mesorregiao = db.session.get(Mesorregiao, CO_MESORREGIAO)
            if not mesorregiao:
                return {"erro": "Mesorregião não encontrada"}, 404
            return marshal(mesorregiao, mesorregiao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar mesorregião")
            abort(500, description="Erro ao buscar mesorregião no banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar mesorregião")
            abort(500, description="Erro interno inesperado.")

    def put(self, CO_MESORREGIAO):
        logger.info(f"PUT - Mesorregião {CO_MESORREGIAO}")
        schema = MesorregiaoSchema()
        dados = request.get_json()

        try:
            mesorregiao = db.session.get(Mesorregiao, CO_MESORREGIAO)
            if not mesorregiao:
                return {"erro": "Mesorregião não encontrada"}, 404

            atualizados = schema.load(dados, partial=True)
            for campo, valor in atualizados.items():
                setattr(mesorregiao, campo, valor)

            db.session.commit()
            return marshal(mesorregiao, mesorregiao_fields), 200

        except ValidationError as err:
            return {"erro": "Dados inválidos", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao atualizar mesorregião")
            db.session.rollback()
            abort(500, description="Erro ao atualizar mesorregião.")
        except Exception:
            log_exception("Erro inesperado ao atualizar mesorregião")
            abort(500, description="Erro interno inesperado.")

    def delete(self, CO_MESORREGIAO):
        logger.info(f"DELETE - Mesorregião {CO_MESORREGIAO}")
        try:
            mesorregiao = db.session.get(Mesorregiao, CO_MESORREGIAO)
            if not mesorregiao:
                return {"erro": "Mesorregião não encontrada"}, 404

            db.session.delete(mesorregiao)
            db.session.commit()
            return {"mensagem": "Mesorregião removida com sucesso"}, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao remover mesorregião")
            db.session.rollback()
            abort(500, description="Erro ao remover mesorregião.")
        except Exception:
            log_exception("Erro inesperado ao remover mesorregião")
            abort(500, description="Erro interno inesperado.")
