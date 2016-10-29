from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class Tarefa(models.Model):
	inicio = models.DateTimeField(null=False, blank=False)
	termino = models.DateTimeField(null=False, blank=False)
	nome = models.CharField(max_length=50, null=False, blank=False)
	descricao = models.TextField(null=True, blank=True)
	encerrada = models.BooleanField(default=False)
	usuario = models.ForeignKey(User, null=False, blank=False)