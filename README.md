# 🏫 Django Coding Classroom

[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-7952B3?logo=bootstrap)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive online coding classroom platform built with Django that enables seamless assignment management, code submission, and automated evaluation for programming courses.

![Dashboard Preview](https://via.placeholder.com/800x400/4A6572/FFFFFF?text=Django+Coding+Classroom)

## ✨ Key Features

### 👨‍🏫 For Educators
- **Assignment Management**: Create programming assignments with deadlines
- **Multi-language Support**: Python, Java, and C++ assignments
- **Automated Evaluation**: Real-time code execution and output validation
- **Submission Review**: Grade submissions with detailed feedback
- **Late Submission Tracking**: Automatic late submission detection
- **Class Analytics**: View submission statistics and performance metrics

### 👨‍🎓 For Students
- **Interactive Dashboard**: View all assignments in one place
- **Code Editor**: Built-in code submission interface
- **Instant Feedback**: See code execution results immediately
- **Submission History**: Track all past submissions and grades
- **Deadline Tracking**: Never miss assignment deadlines
- **Progress Monitoring**: View personal learning progress

### 🛠️ Technical Features
- **Role-based Access**: Separate interfaces for teachers and students
- **Secure Code Execution**: Sandboxed environment for code evaluation
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Real-time Output**: Live code execution results
- **Database Flexibility**: SQLite (development) / PostgreSQL (production)
- **Session Management**: Secure authentication and authorization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Web browser with JavaScript enabled

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/django-coding-classroom.git
   cd django-coding-classroom


Set Up Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate    # Windows
Install Dependencies

bash
pip install -r requirements.txt
Configure Database

bash
python manage.py makemigrations
python manage.py migrate
Create Superuser (Optional)

bash
python manage.py createsuperuser
Run Development Server

bash
python manage.py runserver
Access the Application
Navigate to http://localhost:8000 and register as a teacher or student.

🏗️ System Architecture
text
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django         │    │   Database      │
│   (Bootstrap 5) │◄──►│   Backend        │◄──►│   (SQLite)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         │                        ▼
         │                ┌──────────────────┐
         │                │   Code Executor  │
         │                │   (Python/Java/  │
         │                │      C++)        │
         │                └──────────────────┘
         ▼
   ┌─────────────┐
   │   Browser   │
   │   Client    │
   └─────────────┘
📁 Project Structure
text
django-coding-classroom/
├── classroom/                 # Main Django application
│   ├── models/              # Database models
│   ├── views/               # Application views
│   ├── templates/           # HTML templates
│   │   ├── teacher/         # Teacher-specific templates
│   │   ├── student/         # Student-specific templates
│   │   └── base.html        # Base template
│   ├── executors/           # Code execution engines
│   │   ├── python_executor.py
│   │   ├── java_executor.py
│   │   └── cpp_executor.py
│   └── utils/               # Utility functions
├── config/                  # Project configuration
│   ├── settings/           # Settings modules
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   └── urls.py            # Main URL configuration
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── requirements/           # Dependency files
│   ├── base.txt           # Core dependencies
│   ├── development.txt    # Development dependencies
│   └── production.txt     # Production dependencies
└── manage.py              # Django management script
🛠️ Technology Stack
Backend
Framework: Django 4.2

Language: Python 3.8+

Database: SQLite (Development), PostgreSQL (Production)

Authentication: Django Auth with session management

Frontend
UI Framework: Bootstrap 5.1.3

Templating: Django Templates

Icons: Bootstrap Icons

Styling: Custom CSS with Bootstrap

Code Execution
Python: Built-in interpreter

Java: JDK with javac compiler

C++: G++ compiler

Security: Subprocess with timeout and resource limits

🗃️ Database Models
Core Models
python
# User Profile extending Django User
class Profile(models.Model):
    USER_ROLES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    
# Assignment created by teachers
class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

# Student submissions
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    output = models.TextField(blank=True, null=True)
    errors = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    is_late = models.BooleanField(default=False)
🎯 Usage Guide
For Teachers
Registration & Login

Register with teacher role

Access teacher dashboard

Create Assignments

Click "Create Assignment" in dashboard

Set title, description, programming language, and deadline

Publish assignment for students

Review Submissions

View all submissions for each assignment

Execute student code to see output

Provide marks and constructive feedback

Track late submissions

For Students
Registration & Login

Register with student role

Access student dashboard

View Assignments

See all available assignments

Check deadlines and requirements

View personal submission status

Submit Solutions

Click on assignment to submit

Write code in built-in editor or upload file

Submit and view immediate execution results

Check teacher feedback and grades

⚙️ Configuration
Development Settings
Create config/settings/development.py:

python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Code execution settings
CODE_EXECUTION_TIMEOUT = 10
MAX_CODE_LENGTH = 10000
Production Deployment
Environment Setup

bash
# Set environment variables
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com
Database Configuration

python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'classroom_db',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Static Files

bash
python manage.py collectstatic
🔒 Security Features
Role-based Access Control: Separate permissions for teachers and students

Secure Code Execution: Time and memory limits on code execution

SQL Injection Protection: Django ORM with parameterized queries

XSS Protection: Django template auto-escaping

CSRF Protection: Built-in CSRF tokens

Session Security: Secure session management

🧪 Testing
Running Tests
bash
# Run all tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report

# Run specific app tests
python manage.py test classroom
Test Coverage
User authentication and authorization

Assignment creation and management

Code submission and execution

Role-based access control

Form validation and error handling

🐳 Docker Support
Using Docker Compose
yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
Build and Run
bash
docker-compose up --build
🤝 Contributing
We welcome contributions from the community! Here's how you can help:

Fork the Repository

Create a Feature Branch

bash
git checkout -b feature/amazing-feature
Commit Your Changes

bash
git commit -m 'Add amazing feature'
Push to the Branch

bash
git push origin feature/amazing-feature
Open a Pull Request

Development Guidelines
Follow PEP 8 for Python code

Write tests for new features

Update documentation accordingly

Use meaningful commit messages

🐛 Troubleshooting
Common Issues
Migration Problems

bash
# Reset migrations
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
Static Files Not Loading

bash
python manage.py collectstatic
Code Execution Failing

Ensure Python/Java/C++ are installed

Check file permissions in temp directories

Verify code execution timeout settings

Permission Errors

Confirm user has correct role in profile

Check authentication middleware configuration

📈 Future Roadmap
Planned Features
Docker-based Sandbox - Secure code execution environment

REST API - Mobile app and third-party integrations

Real-time Notifications - Live updates for new assignments and grades

Plagiarism Detection - Code similarity analysis

Advanced Analytics - Detailed performance metrics and insights

Group Assignments - Support for team projects

Code Review System - Peer review capabilities

Integration with Git - Version control for assignments

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Contributors
Your Name - Initial work - @yourusername

📞 Support
Documentation: Project Wiki

Issue Tracker: GitHub Issues

Email Support: your-email@example.com

<div align="center">
⭐ Star us on GitHub if you find this project useful!
Happy Coding! 🎉

</div>