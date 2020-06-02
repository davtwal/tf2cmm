from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('createParty/', views.createParty, name='createParty'),
  path('<slug:party_id>/', views.party, name='party'),
]
