from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Card(models.Model):
  name = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  price = models.IntegerField(validators=[MinValueValidator(0)])
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('card-detail', kwargs={'card_id': self.id})
  
class Photo(models.Model):
  url = models.CharField(max_length=250)
  card = models.OneToOneField(Card, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for card_id: {self.card_id} @{self.url}"