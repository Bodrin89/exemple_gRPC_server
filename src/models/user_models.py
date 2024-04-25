from enum import Enum

from tortoise import fields, models


class UserModels(models.Model):
    class Meta:
        table = 'users'
        ordering = ['id']

    class Role(str, Enum):
        USER = 'user'
        ADMIN = 'admin'

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    role: Role = fields.CharEnumField(Role, default=Role.USER)
    subscription = fields.BooleanField(default=False)
