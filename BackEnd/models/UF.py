from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer
from helpers.database import db
from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields


uf_fields = {
    'CO_UF': flaskFields.Integer,
    'SG_UF': flaskFields.String,
    'NO_UF': flaskFields.String
}


def validate_positive(value):
    if value < 0:
        raise ValidationError("O valor deve ser um número inteiro não negativo.")
    

class UF(db.Model):
    __tablename__ = "ufs"

    CO_UF: Mapped[int] = mapped_column(Integer, primary_key=True)
    SG_UF: Mapped[str] = mapped_column(String(2), nullable=False)
    NO_UF: Mapped[str] = mapped_column(Text, nullable=False)



class UFSchema(Schema):
    CO_UF = fields.Int(
        required=True,
        validate=validate_positive,
        error_messages={
            "required": "O campo CO_UF é obrigatório.",
            "null": "O campo CO_UF não pode ser nulo."
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
    NO_UF = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=50),
        error_messages={
            "required": "O campo NO_UF é obrigatório.",
            "null": "O campo NO_UF não pode ser nulo.",
            "validator_failed": "O campo NO_UF deve ter entre 2 e 50 caracteres."
        }
    )
