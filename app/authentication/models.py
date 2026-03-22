from tortoise import fields, models


class UserDB(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, min_length=3, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    address = fields.CharField(max_length=255, null=True)
    hashed_password = fields.CharField(max_length=255)
    