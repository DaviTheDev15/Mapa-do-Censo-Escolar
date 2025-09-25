from helpers.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey
from models.UF import UF 
from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields


mesorregiao_fields = {
    'CO_MESORREGIAO': flaskFields.Integer,
    'NO_MESORREGIAO': flaskFields.String,
    'CO_UF': flaskFields.Integer
}


def validate_positive(value):
    if value < 0:
        raise ValidationError("O valor deve ser um número inteiro não negativo.")


class Mesorregiao(db.Model):
    __tablename__ = "mesorregioes"

    CO_MESORREGIAO: Mapped[int] = mapped_column(Integer, primary_key=True)
    NO_MESORREGIAO: Mapped[str] = mapped_column(Text, nullable=False)
    CO_UF: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ufs.CO_UF"),
        nullable=False
    )


class MesorregiaoSchema(Schema):
    CO_MESORREGIAO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MESORREGIAO é obrigatório.",
            "null": "O campo CO_MESORREGIAO não pode ser nulo."
        }
    )
    NO_MESORREGIAO = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O campo NO_MESORREGIAO é obrigatório.",
            "null": "O campo NO_MESORREGIAO não pode ser nulo.",
            "validator_failed": "O campo NO_MESORREGIAO deve ter entre 3 e 255 caracteres."
        }
    )
    CO_UF = fields.Int(
        required=True, 
        validate=validate.Length(min=2, max=2),
        error_messages={
            "required": "O campo CO_UF é obrigatório.",
            "null": "O campo CO_UF não pode ser nulo.",
            "validator_failed": "O campo CO_UF deve ter exatamente 2 caracteres."
        }
    )
