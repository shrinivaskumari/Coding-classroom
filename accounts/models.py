from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Extend user with role (Teacher/Student)
class Profile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


from django.utils import timezone
from datetime import timedelta

class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now() + timedelta(days=7))  # default 1 week


    def __str__(self):
        return self.title
        

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    output = models.TextField(blank=True, null=True)   # program stdout
    errors = models.TextField(blank=True, null=True)   # program stderr
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"