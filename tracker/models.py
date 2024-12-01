from django.db import models
from django.db.models import Q, Count


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    def busy():
        queryset = Employee.objects.annotate(
            active_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__open=True))
        ).order_by('-active_tasks')
        return queryset

    def least_busy():
        queryset = Employee.objects.annotate(
            active_tasks=Count('assigned_tasks', filter=Q(assigned_tasks__open=True))
        ).order_by('active_tasks')
        return queryset

class Board(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    parent_task = models.ForeignKey('self',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='subtasks')
    assignee = models.ForeignKey(Employee,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='assigned_tasks') 
    due_date = models.DateField(null=True,
                                 blank=True)
    open = models.BooleanField(default=True)
    board = models.ForeignKey(Board,
                               related_name='tasks',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.title

    def important():
        unassigned = Task.objects.filter(
             assignee__isnull=True,
             parent_task__isnull=False,
             parent_task__assignee__isnull=False,
        )
        return unassigned
