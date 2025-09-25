from helpers.database import db
from models.Microrregiao import Microrregiao
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, ForeignKey
from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields


municipio_fields = {
    'CO_MUNICIPIO': flaskFields.Integer,
    'NO_MUNICIPIO': flaskFields.String,
    'CO_MICRORREGIAO': flaskFields.Integer
}


def validate_positive(value):
    if value < 0:
        raise ValidationError("O valor deve ser um número inteiro não negativo.")


class Municipio(db.Model):
    __tablename__ = "municipios"

    CO_MUNICIPIO: Mapped[int] = mapped_column(Integer, primary_key=True)
    NO_MUNICIPIO: Mapped[str] = mapped_column(Text, nullable=False)
    CO_MICRORREGIAO: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("microrregioes.CO_MICRORREGIAO"),
        nullable=True
    )


class MunicipioSchema(Schema):
    CO_MUNICIPIO = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MUNICIPIO é obrigatório.",
            "null": "O campo CO_MUNICIPIO não pode ser nulo."
        }
    )
    NO_MUNICIPIO = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=255),
        error_messages={
            "required": "O campo NO_MUNICIPIO é obrigatório.",
            "null": "O campo NO_MUNICIPIOO não pode ser nulo.",
            "validator_failed": "O campo NO_MUNICIPIO deve ter entre 3 e 255 caracteres."
        }
    )
    CO_MICRORREGIAO = fields.Int(
        required=True, 
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_MICRORREGIAO é obrigatório.",
            "null": "O campo CO_MICRORREGIAO não pode ser nulo.",
            "validator_failed": "O campo CO_MICRORREGIAO deve ter exatamente 2 caracteres."
        }
    )
