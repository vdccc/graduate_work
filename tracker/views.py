from django.shortcuts import render
from django.db.models import Q, Count
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from tracker.serializers import BoardSerializer, EmployeeSerializer, TaskSerializer
from tracker.models import Employee, Board, Task


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    @action(detail=True)
    def list_tasks(self, request, pk=None):
        queryset = Task.objects.filter(board_id=pk)
        serializer = TaskSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True)
    def busy(self, request):
        queryset = Employee.objects.annotate(
            active_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__status='Open'))
        ).order_by('-active_tasks')
        serializer = EmployeeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True)
    def candidate(self, request):
        pass


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

