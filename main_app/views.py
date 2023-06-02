from django.shortcuts import render

# Add the following import
from django.http import HttpResponse

# Define the home view

# Add the Cat class & list and view function below the imports
class Card:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, brand, description, price):
    self.name = name
    self.brand = brand
    self.description = description
    self.price = price

cards = [
  Card('MJ', 'NBA', 'Mcheal Jordan collectible card', 300),
  Card('Pikachu', 'Pokemon', 'Yellow', 0),
  # Card('Fancy', 'bombay', 'Happy fluff ball.', 4),
  # Card('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]


def about(request):
  return render(request, 'about.html')

def home(request):
  return HttpResponse(request, 'home.html')

# Add new view
def card_index(request):
  return render(request, 'cards/index.html', { 'cards': cards })