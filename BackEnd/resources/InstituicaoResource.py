from flask import request, abort
from flask_restful import Resource, marshal
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from helpers.database import db
from helpers.logging import logger, log_exception
from models.InstituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema, instiuicao_fields


class InstituicoesResource(Resource):
    def get(self):
        logger.info("GET ALL- Listagem de instituições")

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        ano = request.args.get("ano", type=int)

        try:
            query = db.select(InstituicaoEnsino)
            instituicoes = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()
            return marshal(instituicoes, instiuicao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar instituições")
            db.session.rollback()
            abort(500, description="Erro ao buscar instituições no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar instituições")
            abort(500, description="Erro interno inesperado.")

    def post(self):
        logger.info("POST - Nova instituição")

        schema = InstituicaoEnsinoSchema()
        dados = request.get_json()

        try:
            validado = schema.load(dados)
            nova_instituicao = InstituicaoEnsino(**validado)
            db.session.add(nova_instituicao)
            db.session.commit()

            logger.info(f"Instituição {nova_instituicao.CO_ENTIDADE} criada com sucesso!")
            return marshal(nova_instituicao, instiuicao_fields), 201

        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {
                "mensagem": "Erro de validação nos dados enviados.",
                "detalhes": err.messages
            }, 422

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao inserir instituição")
            db.session.rollback()
            abort(500, description="Erro ao inserir dados no banco.")

        except Exception:
            log_exception("Erro inesperado no POST instituição")
            abort(500, description="Erro interno inesperado.")


class InstituicaoResource(Resource):
    def get(self, CO_ENTIDADE, NU_ANO_CENSO):
        logger.info(f"GET BY CO_ENTIDADE & ANO- Instituição ({CO_ENTIDADE}, {NU_ANO_CENSO})")

        try:
            inst = db.session.get(InstituicaoEnsino, {"CO_ENTIDADE": CO_ENTIDADE, "NU_ANO_CENSO": NU_ANO_CENSO})
            if not inst:
                return {"erro": "Instituição não encontrada."}, 404

            return marshal(inst, instiuicao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar instituição")
            db.session.rollback()
            abort(500, description="Erro ao buscar a instituição no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar instituição")
            abort(500, description="Erro interno inesperado.")

    def put(self, CO_ENTIDADE, NU_ANO_CENSO):
        logger.info(f"PUT - Instituição ({CO_ENTIDADE}, {NU_ANO_CENSO})")

        schema = InstituicaoEnsinoSchema()
        dados = request.get_json()

        try:
            inst = db.session.get(InstituicaoEnsino, {"CO_ENTIDADE": CO_ENTIDADE, "NU_ANO_CENSO": NU_ANO_CENSO})
            if not inst:
                return {"erro": "Instituição não encontrada."}, 404

            atualizados = schema.load(dados, partial=True)

            for campo, valor in atualizados.items():
                setattr(inst, campo, valor)

            db.session.commit()
            logger.info(f"Instituição ({CO_ENTIDADE}, {NU_ANO_CENSO}) atualizada com sucesso")
            return marshal(inst, instiuicao_fields), 200

        except ValidationError as err:
            logger.warning(f"Erro de validação: {err.messages}")
            return {"erro": "Dados inválidos.", "detalhes": err.messages}, 422

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao atualizar instituição")
            db.session.rollback()
            abort(500, description="Erro ao atualizar a instituição.")

        except Exception:
            log_exception("Erro inesperado ao atualizar instituição")
            abort(500, description="Erro interno inesperado.")

    def delete(self, CO_ENTIDADE, NU_ANO_CENSO):
        logger.info(f"DELETE - Instituição ({CO_ENTIDADE}, {NU_ANO_CENSO})")

        try:
            inst = db.session.get(InstituicaoEnsino, {"CO_ENTIDADE": CO_ENTIDADE, "NU_ANO_CENSO": NU_ANO_CENSO})
            if not inst:
                return {"erro": "Instituição não encontrada."}, 404

            db.session.delete(inst)
            db.session.commit()

            logger.info(f"Instituição ({CO_ENTIDADE}, {NU_ANO_CENSO}) removida com sucesso")
            return {"mensagem": "Instituição removida com sucesso."}, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao remover instituição")
            db.session.rollback()
            abort(500, description="Erro ao remover a instituição.")

        except Exception:
            log_exception("Erro inesperado ao remover instituição")
            abort(500, description="Erro interno inesperado.")


class MatriculasPorEstadoResource(Resource):
    def get(self):
        ano = request.args.get("ano", type=int)
        logger.info("GET - Matrículas por estado")

        if not ano:
            return {"erro": "Parâmetro 'ano' é obrigatório."}, 400

        try:
            resultados = db.session.execute(
                db.select(
                    InstituicaoEnsino.SG_UF,
                    db.func.sum(
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_BAS, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_EJA, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_ESP, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_FUND, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_INF, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_MED, 0) +
                        db.func.coalesce(InstituicaoEnsino.QT_MAT_PROF, 0)
                    ).label("total_matriculas")
                ).where(InstituicaoEnsino.NU_ANO_CENSO == ano)
                .group_by(InstituicaoEnsino.SG_UF)
                .order_by(InstituicaoEnsino.SG_UF)
            ).all()

            resposta = {uf: total for uf, total in resultados}
            return resposta, 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar matrículas por estado")
            db.session.rollback()
            abort(500, description="Erro ao consultar matrículas.")

        except Exception:
            log_exception("Erro inesperado ao buscar matrículas")
            abort(500, description="Erro interno inesperado.")

class InstituicaoAnoResource(Resource):
    def get(self, NU_ANO_CENSO):
        logger.info(f"GET ALL BY ANO- Instituições do ano {NU_ANO_CENSO}")

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        try:
            query = db.select(InstituicaoEnsino).where(
                InstituicaoEnsino.NU_ANO_CENSO == NU_ANO_CENSO
            ).order_by(InstituicaoEnsino.CO_ENTIDADE)

            instituicoes = db.session.execute(
                query.offset((page - 1) * per_page).limit(per_page)
            ).scalars().all()

            if not instituicoes:
                return {"erro": "Nenhuma instituição encontrada para este ano."}, 404

            return marshal(instituicoes, instiuicao_fields), 200

        except SQLAlchemyError:
            log_exception("Erro SQLAlchemy ao buscar instituições por ano")
            db.session.rollback()
            abort(500, description="Erro ao buscar instituições no banco de dados.")

        except Exception:
            log_exception("Erro inesperado ao buscar instituições por ano")
            abort(500, description="Erro interno inesperado.")

