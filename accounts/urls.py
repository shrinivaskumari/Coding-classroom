from django.urls import path
from .import views

urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    # Teacher
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/review/<int:assignment_id>/', views.review_submissions, name='review_submissions'),

    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
             ]