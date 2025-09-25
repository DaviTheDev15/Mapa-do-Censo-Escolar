from helpers.database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey
from models.Mesorregiao import Mesorregiao
from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields


microrregiao_fields = {
    'CO_MICRORREGIAO': flaskFields.Integer,
    'NO_MICRORREGIAO': flaskFields.String,
    'CO_MESORREGIAO': flaskFields.Integer
}


def validate_positive(value):
    if value < 0:
        raise ValidationError("O valor deve ser um número inteiro não negativo.")


class Microrregiao(db.Model):
    __tablename__ = "microrregioes"

    CO_MICRORREGIAO: Mapped[int] = mapped_column(Integer, primary_key=True)
    NO_MICRORREGIAO: Mapped[str] = mapped_column(Text, nullable=False)
    CO_MESORREGIAO: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mesorregioes.CO_MESORREGIAO"),
        nullable=False
    )


class MicrorregiaoSchema(Schema):
    CO_MICRORREGIAO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MICRORREGIAO é obrigatório.",
            "null": "O campo CO_MICRORREGIAO não pode ser nulo."
        }
    )
    NO_MICRORREGIAO = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O campo CO_MICRORREGIAO é obrigatório.",
            "null": "O campo CO_MICRORREGIAO não pode ser nulo.",
            "validator_failed": "O campo CO_MICRORREGIAO deve ter entre 3 e 255 caracteres."
        }
    )
    CO_MESORREGIAO = fields.Int(
        required=True, 
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MESORREGIAO é obrigatório.",
            "null": "O campo CO_MESORREGIAO não pode ser nulo.",
            "validator_failed": "O campo CO_MESORREGIAO deve ter exatamente 2 caracteres."
        }
    )
