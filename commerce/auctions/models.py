from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Category(models.Model):
    korean_name = models.CharField(max_length=64, default='')
    english_name = models.CharField(max_length=64, default='')

    def __str__(self):
        return f"{self.korean_name}"

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    photo = models.URLField(blank=True, default="https://res.cloudinary.com/dxeibizaf/image/upload/v1616122320/auctions/27_a1hx87.jpg")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.seller}, {self.title}, {self.description}, {self.starting_price}, {self.photo}, {self.active}, {self.winner}, {self.category}"
