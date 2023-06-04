from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('cards/', views.card_index, name='card-index'),
  path('cards/<int:card_id>/', views.card_detail, name='card-detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('cards/create/', views.CardCreate.as_view(), name='card-create'),
]