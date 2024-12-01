from django.test import TestCase
from tracker.models import Employee, Board, Task

# Create your tests here.


class TestTaskCreation(TestCase):
    def setUp(self):
        employeeA = Employee.objects.create(
            full_name="John Doe", position="test subject"
        )
        employeeB = Employee.objects.create(
            full_name="Jack Poe", position="test supervisor"
        )
        board = Board.objects.create(title="Main")
        taskC = Task.objects.create(
            title="Test Task C",
            assignee=employeeA,
            board=board,
        )
        taskD = Task.objects.create(
            title="Test Task D",
            board=board,
            parent_task=taskC,
        )
        taskA = Task.objects.create(
            title="Test Task A",
            assignee=employeeA,
            board=board,
            parent_task=taskC,
        )
        taskB = Task.objects.create(
            title="Test Task B",
            assignee=employeeB,
            board=board,
            parent_task=taskC,
        )

    def test_board_has_tasks(self):
        tasksAll = Task.objects.all()
        board = Board.objects.get(title="Main")
        boardTasks = board.tasks.all()
        for task in tasksAll:
            self.assertIn(task, boardTasks)

    def test_busy_employees(self):
        busyness = {
            "John Doe": 2,
            "Jack Poe": 1,
        }
        busyEmployees = Employee.busy().all()
        self.assertEqual(len(busyEmployees), 2)
        for busy in busyEmployees:
            self.assertEqual(busy.active_tasks, busyness[busy.full_name])

    def test_least_busy_employees(self):
        employees = Employee.least_busy()
        self.assertEqual(employees[0].full_name, "Jack Poe")

    def test_important_tasks(self):
        tasks = Task.important().all()
        self.assertEqual(tasks[0].title, "Test Task D")
