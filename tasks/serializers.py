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

    def validate(self, data):
        inicio = data.get('inicio')
        termino = data.get('termino')
        if inicio > termino:
            msg = u'Data de início deve ser menor ou igual a data de término.'
            raise serializers.ValidationError({
                'erro': msg
            })
        return data
