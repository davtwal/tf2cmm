import base64
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import exceptions


# Create your views here.
from .models import Party

def index(request):
  party_list = Party.objects.all()
  context = {'party_list': party_list}
  return render(request, 'party/index.html', context)

def party(request, party_id, password=0):
  party = get_object_or_404(Party, pk=party_id)
  return render(request, 'party/party.html', {'party_id': party_id})

def createParty(request):
  while True:
    # TODO: Make this limit less fucky
    b64_max_b = '________'.encode('ascii')
    id_max = int.from_bytes(base64.urlsafe_b64decode(b64_max_b), byteorder='big')
    new_base10_id = random.randint(0, id_max)
    new_id = base64.urlsafe_b64encode(int.to_bytes(new_base10_id, 6, byteorder='big')).decode('ascii')
    try:
      Party.objects.get(pk=new_id)
    except exceptions.ObjectDoesNotExist:
      new_party = Party(pk=new_id)
      new_party.save()
      return redirect('party', party_id=new_id)