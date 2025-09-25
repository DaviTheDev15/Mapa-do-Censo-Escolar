from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields
from helpers.database import db
from models.UF import UF
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio


instiuicao_fields = {
    'NU_ANO_CENSO': flaskFields.Integer,
    'NO_REGIAO': flaskFields.String,
    'CO_REGIAO': flaskFields.Integer,
    'NO_UF': flaskFields.String,
    'SG_UF': flaskFields.String,
    'CO_UF': flaskFields.Integer,
    'NO_MUNICIPIO': flaskFields.String,
    'CO_MUNICIPIO': flaskFields.Integer,
    'CO_MESORREGIAO': flaskFields.Integer,
    'CO_MICRORREGIAO': flaskFields.Integer,
    'NO_ENTIDADE': flaskFields.String,
    'CO_ENTIDADE': flaskFields.Integer,
    'QT_MAT_BAS': flaskFields.Integer,
    'QT_MAT_EJA': flaskFields.Integer,
    'QT_MAT_ESP': flaskFields.Integer,
    'QT_MAT_FUND': flaskFields.Integer,
    'QT_MAT_INF': flaskFields.Integer,
    'QT_MAT_MED': flaskFields.Integer,
    'QT_MAT_PROF': flaskFields.Integer,
}


def validate_positive(value):
    if value < 0:
        raise ValidationError("O valor deve ser um número inteiro não negativo.")


class InstituicaoEnsino(db.Model):
    __tablename__ = "instituicoes"

    NU_ANO_CENSO: Mapped[int] = mapped_column(primary_key=True)
    CO_ENTIDADE: Mapped[int] = mapped_column(primary_key=True)
    NO_REGIAO: Mapped[str] = mapped_column(nullable=False)
    CO_REGIAO: Mapped[int] = mapped_column(nullable=False)
    NO_UF: Mapped[str] = mapped_column(nullable=False)
    SG_UF: Mapped[str] = mapped_column(nullable=False)
    CO_UF: Mapped[int] = mapped_column(ForeignKey("ufs.CO_UF"), nullable=False)
    NO_MUNICIPIO: Mapped[str] = mapped_column(nullable=False)
    CO_MUNICIPIO: Mapped[int] = mapped_column(ForeignKey("municipios.CO_MUNICIPIO"), nullable=False)
    CO_MESORREGIAO: Mapped[int] = mapped_column(ForeignKey("mesorregioes.CO_MESORREGIAO"), nullable=False)
    CO_MICRORREGIAO: Mapped[int] = mapped_column(ForeignKey("microrregioes.CO_MICRORREGIAO"), nullable=False)
    NO_ENTIDADE: Mapped[str] = mapped_column(nullable=False)
    QT_MAT_BAS: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_EJA: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_ESP: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_FUND: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_INF: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_MED: Mapped[int] = mapped_column(nullable=False)
    QT_MAT_PROF: Mapped[int] = mapped_column(nullable=False)


class InstituicaoEnsinoSchema(Schema):
    NU_ANO_CENSO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo NU_ANO_CENSO é obrigatório.",
            "null": "O campo NU_ANO_CENSO não pode ser nulo."
        }
    )
    NO_REGIAO = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=20), 
        error_messages={
            "required": "O campo NO_REGIAO é obrigatório.",
            "null": "O campo NO_REGIAO não pode ser nulo.",
            "validator_failed": "O campo NO_REGIAO deve ter entre 3 e 20 caracteres."
        }
    )
    CO_REGIAO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_REGIAO é obrigatório.",
            "null": "O campo CO_REGIAO não pode ser nulo."
        }
    )
    NO_UF = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=50),
        error_messages={
            "required": "O campo NO_UF é obrigatório.",
            "null": "O campo NO_UF não pode ser nulo.",
            "validator_failed": "O campo NO_UF deve ter entre 2 e 50 caracteres."
        }
    )
    SG_UF = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=2),
        error_messages={
            "required": "O campo SG_UF é obrigatório.",
            "null": "O campo SG_UF não pode ser nulo.",
            "validator_failed": "O campo SG_UF deve ter exatamente 2 caracteres."
        }
    )
    CO_UF = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_UF é obrigatório.",
            "null": "O campo CO_UF não pode ser nulo."
        }
    )
    NO_MUNICIPIO = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=150),
        error_messages={
            "required": "O campo NO_MUNICIPIO é obrigatório.",
            "null": "O campo NO_MUNICIPIO não pode ser nulo.",
            "validator_failed": "O campo NO_MUNICIPIO deve ter entre 3 e 150 caracteres."
        }
    )
    CO_MUNICIPIO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MUNICIPIO é obrigatório.",
            "null": "O campo CO_MUNICIPIO não pode ser nulo."
        }
    )
    CO_MESORREGIAO = fields.Int(
        required=True, 
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MESORREGIAO é obrigatório.",
            "null": "O campo CO_MESORREGIAO não pode ser nulo."
        }
    )
    CO_MICRORREGIAO = fields.Int(
        required=True, 
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MICRORREGIAO é obrigatório.",
            "null": "O campo CO_MICRORREGIAO não pode ser nulo."
        }
    )
    NO_ENTIDADE = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=100),
        error_messages={
            "required": "O campo NO_ENTIDADE é obrigatório.",
            "null": "O campo NO_ENTIDADE não pode ser nulo.",
            "validator_failed": "O campo NO_ENTIDADE deve ter entre 3 e 100 caracteres."
        }
    )
    CO_ENTIDADE = fields.Int(
        required=True, 
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_ENTIDADE é obrigatório.",
            "null": "O campo CO_ENTIDADE não pode ser nulo."
        }
    )
    QT_MAT_BAS = fields.Int(required=True, validate=validate_positive)
    QT_MAT_EJA = fields.Int(required=True, validate=validate_positive)
    QT_MAT_ESP = fields.Int(required=True, validate=validate_positive)
    QT_MAT_FUND = fields.Int(required=True, validate=validate_positive)
    QT_MAT_INF = fields.Int(required=True, validate=validate_positive)
    QT_MAT_MED = fields.Int(required=True, validate=validate_positive)
    QT_MAT_PROF = fields.Int(required=True, validate=validate_positive)
