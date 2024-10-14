from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    province = models.CharField(max_length=20, blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")  # Changed related_name for clarity
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students_taught")  # Changed related_name for clarity

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Changed related_name for clarity
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')  # Changed related_name for clarity
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

class ProgressReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Progress Report for {self.student.name} on {self.date}"
