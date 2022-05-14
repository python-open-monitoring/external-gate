from tortoise import fields
from tortoise.models import Model


class User(Model):

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    reset_password_md5 = fields.CharField(max_length=255, null=True, blank=True)
    creation_date = fields.data.DatetimeField(auto_now_add=True)
    last_login_date = fields.data.DatetimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        table = "user_user"
