from django.db import models


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


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
    completed = models.BooleanField(default=False)
    board = models.ForeignKey(Board,
                               related_name='tasks',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.title
