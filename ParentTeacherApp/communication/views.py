from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Message, ProgressReport
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm



# communication/views.py

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User



def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})    
   
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('dashboard')  # Changed to redirect to dashboard after login
        else:
            print(f"Form validation failed: {form.errors}")  # Debug form validation errors
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'register.html', {'form': form})




def dashboard(request):
    
    return render(request, 'dashboard.html')


def send_message(request, student_id):
    """Send a message to a parent or teacher"""
    student = Student.objects.get(id=student_id)
    if request.method == "POST":
        content = request.POST['message']
        recipient = student.parent if request.user.groups.filter(name='Teacher').exists() else student.teacher
        Message.objects.create(sender=request.user, recipient=recipient, student=student, content=content)
        return redirect('view_messages', student_id=student.id)
    return render(request, 'send_message.html', {'student': student})


def view_messages(request, student_id):
    """View messages related to a specific student"""
    return render(request, 'view_messages.html', {'messages': messages, 'student': student})

def add_progress_report(request, student_id):
    """Add a progress report for a student"""
    student = Student.objects.get(id=student_id)
    if request.method == "POST":
        report = request.POST['report']
        ProgressReport.objects.create(student=student, report=report)
        return redirect('dashboard')
    return render(request, 'add_progress_report.html', {'student': student})

def login_view(request):
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'This account is inactive.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            print(f"Form validation failed: {form.errors}")  # Debug form validation errors
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'login.html', {'form': form})

    return render(request, 'login.html', {'form': form})
