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
            return Response(
                tarefa.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(tarefa.errors, status=status.HTTP_400_BAD_REQUEST)