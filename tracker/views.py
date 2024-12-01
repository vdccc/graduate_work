from django.shortcuts import render
from django.db.models import Q, Count
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from tracker.serializers import (
    BoardSerializer,
    EmployeeSerializer,
    TaskSerializer,
    PickSerializer,
)
from tracker.models import Employee, Board, Task


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    @action(detail=True)
    def list_tasks(self, request, pk=None):
        queryset = Task.objects.filter(board_id=pk)
        serializer = TaskSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class Pick:
    def __init__(self, task_id, due_date, employee_full_name):
        self.task_id = task_id
        self.due_date = due_date
        self.employee_full_name = employee_full_name


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False)
    def important(self, request):
        queryset = Task.important()
        serializer = TaskSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def pick(self, request):
        tasks = Task.important().all()
        employee = Employee.least_busy().filter(assigned_tasks__lt=3)
        picks = []
        for task in tasks:
            pick = Pick(task.id, task.due_date, employee.full_name)
            picks.append(pick)
        serializer = PickSerializer(picks, many=True, context={"request": request})
        return Response(serializer.data)
