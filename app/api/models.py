from django.db import models
import datetime

# class Subject(models.Model):
#     class Meta:
#         verbose_name = '学科'
#     name = models.CharField(max_length=20)
#     created = models.DateTimeField(default=datetime.datetime.now, verbose_name="作成日")
#     updated = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True, blank=True)
#     created_at = models.CharField(max_length=31, default="system", verbose_name="作成者")
#     updated_at = models.CharField(max_length=31, null=True, blank=True, verbose_name="更新者")

# class User(models.Model):
#     class Meta:
#         verbose_name = 'ユーザー'
#     id = models.BigIntegerField(primary_key=True, verbose_name="GoogleユーザID")
#     subject = models.ForeignKey(Subject,  on_delete=models.SET_NULL, verbose_name="学科")
#     enrollment_class = models.IntegerField(default=None, vaerbose_name="クラス", null=True)
#     is_admin = models.BooleanField(default=False, verbose_name="管理者権限")
#     created = models.DateTimeField(default=datetime.datetime.now, verbose_name="作成日")
#     updated = models.DateTimeField(auto_now=True, verbose_name="更新日", null=True, blank=True)
#     created_at = models.CharField(max_length=31, default="しす", verbose_name="作成者")
#     updated_at = models.CharField(max_length=31, null=True, blank=True, verbose_name="更新者")

class Subject(models.Model):
    class Meta:
        verbose_name = '学科'
    name = models.CharField(max_length=20)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.CharField(max_length=31, default="system")
    updated_at = models.CharField(max_length=31, null=True, blank=True)

class User(models.Model):
    class Meta:
        verbose_name = 'ユーザー'
    id = models.BigIntegerField(primary_key=True)
    subject = models.ForeignKey(Subject,  on_delete=models.SET_NULL, null=True)
    enrollment_class = models.IntegerField(default=None, null=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.CharField(max_length=31, default="system")
    updated_at = models.CharField(max_length=31, null=True, blank=True)


