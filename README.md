📘 Django Assignment Submission System — Complete Documentation
🧩 System Overview\n
A comprehensive role-based web application built with Django that enables teachers to create programming assignments and students to submit solutions. Features code execution, automated output capture, feedback system, and submission tracking.

🏗️ System Architecture
🔄 Data Flow Architecture
text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│   Django    │───▶│  Database   │
│ (Browser)   │    │   Server    │    │ (SQLite)    │
└─────────────┘    └─────────────┘    └─────────────┘
                         │
                         ▼
                 ┌─────────────┐
                 │ Code Executor│
                 │ (Python/Java│
                 │   /C++)     │
                 └─────────────┘
🗃️ Database Schema
python
# Core Models Structure
User (Django Auth)
├── username, email, password
├── first_name, last_name
└── date_joined, last_login

Profile (User Extension)
├── user (OneToOne)
└── role (teacher/student)

Assignment
├── teacher (ForeignKey → User)
├── title, description, language
├── created_at, deadline
└── submissions (reverse relation)

Submission
├── assignment (ForeignKey)
├── student (ForeignKey → User)
├── code, output, errors
├── submitted_at, marks, feedback
└── is_late (boolean)
🚀 Quick Start Guide
📋 Prerequisites
bash
Python 3.8+
Django 4.2+
Git
Web browser with JavaScript
⚡ Installation Steps
bash
# 1. Clone and setup environment
git clone https://github.com/your-org/assignment-system.git
cd assignment-system
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Database setup
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
🔧 Configuration
Create config/settings_local.py:

python
# Development settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
👥 User Role Matrix
Role	Dashboard Access	Assignment Actions	Submission Actions
👨‍🏫 Teacher	Create assignments, View all submissions	Create, Edit, Delete	Grade, Provide feedback
👨‍🎓 Student	View assignments, Personal submissions	None	Submit code, View feedback
📊 Core Models Deep Dive
🎯 Profile Model
python
class Profile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_student(self):
        return self.role == 'student'
📝 Assignment Model
python
class Assignment(models.Model):
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('java', 'Java'),
        ('cpp', 'C++'),
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    
    def is_past_deadline(self):
        return timezone.now() > self.deadline
📤 Submission Model
python
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
    
    def save(self, *args, **kwargs):
        # Auto-calculate late submission
        if self.assignment.deadline and self.submitted_at:
            self.is_late = self.submitted_at > self.assignment.deadline
        super().save(*args, **kwargs)
🔄 Views & URL Structure
🛣️ URL Patterns
python
# urls.py
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Teacher routes
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assignment/create/', views.create_assignment, name='create_assignment'),
    path('submissions/<int:assignment_id>/', views.review_submissions, name='review_submissions'),
    
    # Student routes  
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
]
👁️ View Logic Examples
python
def student_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
        return redirect('login')
    
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    
    assignments = Assignment.objects.all()
    submissions = Submission.objects.filter(student=request.user)
    
    return render(request, 'student_dashboard.html', {
        'assignments': assignments,
        'submissions': submissions
    })
🖥️ Code Execution Engine
⚙️ Execution Workflow
python
def execute_code(code, language):
    """
    Execute code in specified language and return results
    """
    if language == 'python':
        return execute_python(code)
    elif language == 'java':
        return execute_java(code)
    elif language == 'cpp':
        return execute_cpp(code)
    else:
        return None, "Unsupported language"

def execute_python(code):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute and capture output
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Cleanup
        os.unlink(temp_file)
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return None, "Execution timeout"
    except Exception as e:
        return None, f"Execution error: {str(e)}"
🎨 Frontend Components
🏗️ Base Template Structure
html
<!DOCTYPE html>
<html>
<head>
    <title>Assignment System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Assignment System</a>
            <!-- Dynamic menu based on user role -->
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
📱 Student Dashboard Component
html
<div class="row">
    <div class="col-md-8">
        <h3>Available Assignments</h3>
        {% for assignment in assignments %}
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{{ assignment.title }}</h5>
                <p class="card-text">{{ assignment.description|truncatewords:30 }}</p>
                <span class="badge bg-secondary">{{ assignment.language }}</span>
                <a href="{% url 'submit_assignment' assignment.id %}" class="btn btn-primary btn-sm">Submit Solution</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
🔒 Security Features
🛡️ Authentication & Authorization
python
# Decorators for role-based access
def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
            return HttpResponseForbidden("Teacher access required")
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            return HttpResponseForbidden("Student access required")
        return view_func(request, *args, **kwargs)
    return wrapper
📈 Performance Optimizations
🗃️ Database Optimization
python
# Use select_related and prefetch_related
assignments = Assignment.objects.select_related('teacher').prefetch_related('submission_set')

# Efficient querying for dashboard
submissions = Submission.objects.filter(
    assignment=assignment
).select_related('student').only(
    'student__username', 'submitted_at', 'marks'
)
🧪 Testing Strategy
✅ Test Cases Structure
python
class AssignmentTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user('teacher', 'teacher@school.com', 'password')
        self.teacher_profile = Profile.objects.create(user=self.teacher, role='teacher')
        
        self.student = User.objects.create_user('student', 'student@school.com', 'password') 
        self.student_profile = Profile.objects.create(user=self.student, role='student')
    
    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            teacher=self.teacher,
            title="Test Assignment",
            description="Test Description", 
            language="python",
            deadline=timezone.now() + timedelta(days=7)
        )
        self.assertEqual(assignment.teacher, self.teacher)
🚀 Deployment Checklist
📋 Pre-Deployment
Set DEBUG = False

Configure ALLOWED_HOSTS

Set up production database

Collect static files

Configure email backend

Set up error logging

Configure secure HTTPS

🐳 Docker Support (Optional)
dockerfile
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
🔮 Future Roadmap
🎯 Version 2.0 Features
Feature	Status	Description
Docker Sandbox	Planned	Secure code execution environment
REST API	Planned	Mobile app support
Real-time Notifications	Planned	Live updates for submissions
Plagiarism Check	Research	Code similarity detection
Analytics Dashboard	Planned	Submission statistics & trends
🆘 Troubleshooting Guide
❌ Common Issues
Migration Errors: Delete db.sqlite3 and migrations folder, then re-run migrations

Static Files Not Loading: Run python manage.py collectstatic

Code Execution Failing: Check if Python/Java/C++ compilers are installed

Permission Errors: Verify user has correct role in Profile

📞 Support
Documentation: /docs/

Admin Interface: /admin/

GitHub Issues: Project repository

📝 Note: This documentation is continuously updated. Check the docs/ folder for the latest version and additional resources.

give readme file for the git hub of the project
🎓 Django Assignment Submission System
A comprehensive, role-based web application built with Django that enables teachers to create programming assignments and students to submit solutions with automated code execution and feedback system.

https://img.shields.io/badge/Django-4.2-green
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Bootstrap-5.0-purple
https://img.shields.io/badge/License-MIT-yellow

✨ Features
👨‍🏫 For Teachers
Create programming assignments with deadlines

Support for multiple languages (Python, Java, C++)

Review student submissions with code execution results

Provide marks and detailed feedback

Track late submissions automatically

👨‍🎓 For Students
View available assignments with deadlines

Submit code in supported programming languages

See real-time code execution output and errors

Receive marks and feedback from teachers

View submission history

🛠️ Technical Features
Role-based authentication (Teacher/Student)

Secure code execution environment

Automated output and error capture

Responsive Bootstrap 5 UI

SQLite database (easily configurable for PostgreSQL)

Late submission tracking

🚀 Quick Start
Prerequisites
Python 3.8 or higher

Git

Internet browser with JavaScript enabled

Installation
Clone the repository

bash
git clone https://github.com/your-username/django-assignment-system.git
cd django-assignment-system
Set up virtual environment

bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Set up database

bash
python manage.py makemigrations
python manage.py migrate
Create superuser (optional)

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
Access the application

Open http://localhost:8000 in your browser

Register as a Teacher or Student to get started

📁 Project Structure
text
django-assignment-system/
├── assignment_app/          # Main Django application
│   ├── models.py           # Database models (User, Assignment, Submission)
│   ├── views.py            # Application views and logic
│   ├── urls.py             # URL routing
│   └── templates/          # HTML templates
├── config/                 # Django project settings
├── static/                 # CSS, JavaScript, images
├── media/                  # User uploaded files
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
🗃️ Database Models
Core Models
User: Extended Django auth user with profiles

Profile: Role-based user extension (Teacher/Student)

Assignment: Created by teachers with deadlines

Submission: Student submissions with execution results

Example Usage
python
# Create an assignment
assignment = Assignment.objects.create(
    teacher=teacher_user,
    title="Python Basics",
    description="Write a function to calculate factorial",
    language="python",
    deadline=timezone.now() + timedelta(days=7)
)

# Student submission
submission = Submission.objects.create(
    assignment=assignment,
    student=student_user,
    code="def factorial(n): return 1 if n == 0 else n * factorial(n-1)",
    marks=85,
    feedback="Good solution! Consider edge cases."
)
🎮 Usage Guide
For Teachers
Register/Login with Teacher role

Create assignments from the dashboard

Set language, description, and deadline

Review submissions and provide feedback

View all student submissions with execution results

For Students
Register/Login with Student role

View available assignments on dashboard

Submit code in the required language

View execution output and errors immediately

Check feedback and marks from teachers

🖥️ Supported Languages
Language	Execution Method	Requirements
Python	python temp.py	Python installed
Java	javac + java	JDK installed
C++	g++ + executable	G++ compiler
🔧 Configuration
Environment Settings
Create config/settings_local.py for custom settings:

python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Email configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
Production Deployment
For production deployment:

Set DEBUG = False

Configure proper database (PostgreSQL recommended)

Set up static file serving

Configure ALLOWED_HOSTS

Set up HTTPS

🧪 Testing
Run the test suite:

bash
python manage.py test assignment_app
Test coverage includes:

User authentication and authorization

Assignment creation and management

Code submission and execution

Role-based access control

🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

Development Setup
bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# Check code style
flake8 .
🐛 Troubleshooting
Common Issues
Issue: Migration errors

bash
# Solution: Reset migrations
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
Issue: Static files not loading

bash
# Solution: Collect static files
python manage.py collectstatic
Issue: Code execution not working

Ensure Python/Java/C++ compilers are installed

Check execution timeout settings

Verify file permissions

📈 Roadmap
Planned Features
Docker-based secure code execution sandbox

REST API for mobile applications

Real-time notifications

Plagiarism detection

Advanced analytics dashboard

Assignment categories and tags

Bulk assignment operations

👥 Team
Your Name - Initial work - YourUsername

See also the list of contributors who participated in this project.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Django framework and community

Bootstrap for the UI components

Contributors and testers

📞 Support
📧 Email: your-email@example.com

🐛 Issues: GitHub Issues

💬 Discussions: GitHub Discussions

⭐ If you find this project useful, please give it a star on GitHub!

<div align="center">
🚀 Get Started Today!
Installation Guide • Usage Guide • Contributing

</div>
