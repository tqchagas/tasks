# -*- coding: utf-8 -*-
from tasks.models import Tarefa as TarefaModel
from tasks.serializers import TarefaSerializer

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class Tarefa(APIView):

    def get(self, request):
        tarefas = TarefaModel.objects.all()
        tarefas = TarefaSerializer(tarefas, many=True)
        return Response(tarefas.data)

    def post(self, request):
        tarefa = TarefaSerializer(data=request.data)
        if tarefa.is_valid():
            tarefa.usuario = request.user
            tarefa.save(usuario=request.user)
            return Response(
                tarefa.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(tarefa.errors, status=status.HTTP_400_BAD_REQUEST)

class TarefaEncerrada(APIView):

    def post(self, request):
        tarefa = request.data.get('tarefa')

        try:
            tarefa = TarefaModel.objects.get(pk=tarefa, usuario=request.user)
        except TarefaModel.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        tarefa.encerrada = False if tarefa.encerrada else True
        tarefa.save()
        tarefa = TarefaSerializer(tarefa)
        return Response(tarefa.data, status=status.HTTP_200_OK)
