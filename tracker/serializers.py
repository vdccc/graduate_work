from tracker.models import Employee, Board, Task
from rest_framework import serializers


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title"]


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position"]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "parent_task",
            "assignee",
            "due_date",
            "completed",
            "board",
        ]


class PickSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    due_date = serializers.DateField()
    employee_full_name = serializers.CharField(max_length=255)
