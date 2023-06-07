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


class Home(LoginView):
  template_name = 'home.html'


class CardCreate(CreateView):
  model = Card
  fields = ['name', 'brand', 'description', 'price']
  success_url = '/cards/'
  

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)
  
class CardUpdate(UpdateView):
  model = Card
  fields = ['name', 'brand', 'description', 'price']

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
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('card-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

  
S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'brendan-card-collector'

def add_photo(request, card_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, card_id=card_id)
      # Remove old photo if it exists
      card_photo = Photo.objects.filter(card_id=card_id)
      if card_photo.first():
        card_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('card-detail', card_id=card_id)