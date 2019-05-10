from wtforms import ValidationError

from app.models import User


def validate_unique(column, error, table=User):
    def validator(form, field):
        if table.query.filter_by(**{column: field.data}).first() is not None:
            raise ValidationError(error)

    return validator
