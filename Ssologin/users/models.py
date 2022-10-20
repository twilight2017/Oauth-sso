from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    sesa_number = models.CharField(max_length=124, blank=True, null=True)
    user_name = models.CharField(max_length=124, blank=True, null=True)
    password = models.CharField(max_length=124, blank=True, null=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "sesa_number": self.sesa_number,
            "user_name": self.user_name,
            "password": self.password,
        }


class Article(models.Model):
    """Article Model"""
    STATUS_CHOICES = (
        ('p', 'Published'),
        ('d', 'Draft')
    )

    title = models.CharField(verbose_name="TITLE", max_length=90, db_index=True)
    body = models.TextField(verbose_name="BODY", blank=True)
    author = models.ForeignKey(User, verbose_name="AUTHOR", on_delete=models.CASCADE, related_name="articles")
    status = models.CharField(verbose_name="STATUS", max_length=1, choices=STATUS_CHOICES, default='s', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="CREATEDATE", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    objetcs = models.Manager()

