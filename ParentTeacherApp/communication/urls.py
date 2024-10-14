from django.urls import path
from . import views

urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/',views.login_view,name='login'),
     path('dashboard/', views.dashboard, name='dashboard'),
    # path('send_message/<int:student_id>/', views.send_message, name='send_message'),
    # path('view_messages/<int:student_id>/', views.view_messages, name='view_messages'),
    # path('add_progress_report/<int:student_id>/', views.add_progress_report, name='add_progress_report'),
]
