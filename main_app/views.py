from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Card, Photo
import uuid
import boto3
from django.contrib.auth.views import LoginView
# Add the following import
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# Define the home view

# Add the Cat class & list and view function below the imports
# class Card:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, brand, description, price):
#     self.name = name
#     self.brand = brand
#     self.description = description
#     self.price = price

# cards = [
#   Card('MJ', 'NBA', 'Mcheal Jordan collectible card', 300),
#   Card('Pikachu', 'Pokemon', 'Yellow', 0),
#   # Card('Fancy', 'bombay', 'Happy fluff ball.', 4),
#   # Card('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]
class Home(LoginView):
  template_name = 'home.html'


class CardCreate(CreateView):
  model = Card
  fields = '__all__'
  success_url = '/cards/'
  
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  
class CardUpdate(UpdateView):
  model = Card
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['brand', 'description', 'price']

class CardDelete(DeleteView):
  model = Card
  success_url = '/cards/'


def card_detail(request, card_id):
  card = Card.objects.get(id=card_id)
  return render(request, 'cards/detail.html', { 'card': card })


def about(request):
  return render(request, 'about.html')

def home(request):
  return render(request, 'home.html')

# Add new view
@login_required
def card_index(request):
  cards = Card.objects.filter(user=request.user)
  return render(request, 'cards/index.html', { 'cards': cards })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('card-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as: return render(request, 'signup.html', {'form': form, 'error_message': error_message})

  
S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'brendan-card-collector'

def add_photo(request, card_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, card_id=card_id)
      # Remove old photo if it exists
      card_photo = Photo.objects.filter(card_id=card_id)
      if card_photo.first():
        card_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('card-detail', card_id=card_id)