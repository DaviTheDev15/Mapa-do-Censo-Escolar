from flask import request, abort
from flask_restful import Resource, marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from helpers.database import db
from helpers.logging import logger, log_exception
from models.UF import UF, UFSchema, uf_fields


class UFsResource(Resource):
    def get(self):
        logger.info("GET ALL- Listagem de UFs")

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 27))

        try:
            query = db.select(UF).order_by(UF.CO_UF)
            ufs = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()

            logger.info("UFs retornadas com sucesso")
            return marshal(ufs, uf_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar UFs")
            db.session.rollback()
            abort(500, description="Erro ao buscar UFs no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar UFs")
            abort(500, description="Erro interno inesperado.")

    def post(self):
        logger.info("POST - Nova UF")

        schema = UFSchema()
        dados = request.get_json()

        try:
            validado = schema.load(dados)
            nova_uf = UF(**validado)
            db.session.add(nova_uf)
            db.session.commit()

            logger.info(f"UF {nova_uf.CO_UF} criada com sucesso!")
            return marshal(nova_uf, uf_fields), 201

        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"erro": "Dados inválidos.", "detalhes": err.messages}, 422

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao inserir UF")
            db.session.rollback()
            abort(500, description="Erro ao inserir UF no banco.")

        except Exception:
            log_exception("Erro inesperado no POST UF")
            abort(500, description="Erro interno inesperado.")


class UFResource(Resource):
    def get(self, CO_UF):
        logger.info(f"GET BY CO_UF - UF ({CO_UF})")

        try:
            uf = db.session.get(UF, CO_UF)
            if not uf:
                return {"erro": "UF não encontrada."}, 404

            return marshal(uf, uf_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar UF")
            db.session.rollback()
            abort(500, description="Erro ao buscar UF no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar UF")
            abort(500, description="Erro interno inesperado.")

    def put(self, CO_UF):
        logger.info(f"PUT - UF ({CO_UF})")

        schema = UFSchema()
        dados = request.get_json()

        try:
            uf = db.session.get(UF, CO_UF)
            if not uf:
                return {"erro": "UF não encontrada."}, 404

            atualizados = schema.load(dados, partial=True)
            for campo, valor in atualizados.items():
                setattr(uf, campo, valor)

            db.session.commit()
            logger.info(f"UF ({CO_UF}) atualizada com sucesso")
            return marshal(uf, uf_fields), 200

        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"erro": "Dados inválidos.", "detalhes": err.messages}, 422

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao atualizar UF")
            db.session.rollback()
            abort(500, description="Erro ao atualizar UF no banco.")

        except Exception:
            log_exception("Erro inesperado ao atualizar UF")
            abort(500, description="Erro interno inesperado.")

    def delete(self, CO_UF):
        logger.info(f"DELETE - UF ({CO_UF})")

        try:
            uf = db.session.get(UF, CO_UF)
            if not uf:
                return {"erro": "UF não encontrada."}, 404

            db.session.delete(uf)
            db.session.commit()

            logger.info(f"UF ({CO_UF}) removida com sucesso")
            return {"mensagem": "UF removida com sucesso."}, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao remover UF")
            db.session.rollback()
            abort(500, description="Erro ao remover UF no banco.")

        except Exception:
            log_exception("Erro inesperado ao remover UF")
            abort(500, description="Erro interno inesperado.")
