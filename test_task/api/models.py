from django.db import models
from django.contrib.auth.models import AbstractUser

class ApiUser(AbstractUser):
    class Role(models.TextChoices):
        MODERATOR = "MODERATOR", 'Moderator'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    role = models.CharField(max_length=50, choices=Role.choices)
    REQUIRED_FIELDS = ["role"]


class Section(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    teacher = models.ForeignKey(ApiUser, on_delete=models.SET_NULL, null=True, related_name='+')
    students = models.ManyToManyField(ApiUser, through="UserSection")

    def __str__(self):
        return f'{self.title}'


class UserSection(models.Model):

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'({self.section}, {self.student}, {self.date})'