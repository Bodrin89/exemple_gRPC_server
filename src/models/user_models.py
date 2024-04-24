from tortoise import fields, models


class UserModels(models.Model):
    class Meta:
        table = 'users'
        ordering = ['id']

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    subscription = fields.BooleanField(default=False)
