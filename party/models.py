from django.db import models

# Create your models here.

class Party(models.Model):
  id = models.SlugField('party slug', max_length=7, primary_key=True)
  maps = models.TextField('selected maps list')

  def __str__(self):
    return str(self.id)

class Client(models.Model):
  id = models.UUIDField('client steam auth id', primary_key=True)
  party_id = models.ForeignKey(Party, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.client_id)
