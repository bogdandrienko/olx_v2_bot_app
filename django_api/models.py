from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Ad(models.Model):
    # base
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Наименование товара", max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ads/%Y/%m/%d/', blank=True)

    # util
    flag_good = models.BooleanField(default=False, verbose_name="Одобрено")
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "django_api"
        ordering = ('-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
