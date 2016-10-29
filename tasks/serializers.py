# -*- coding: utf-8 -*-
from tasks.models import Tarefa

from rest_framework import serializers



class TarefaSerializer(serializers.ModelSerializer):
    class Meta:

        model = Tarefa

        fields = (
            'inicio',
            'termino',
            'nome',
            'descricao',
            'encerrada'
        )