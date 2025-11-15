from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Profile, Assignment, Submission
import subprocess, tempfile, os

# ------------------------------------------------------
# LOGIN
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # Redirect based on role
            if hasattr(user, 'profile'):
                if user.profile.role == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                return redirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')


# ------------------------------------------------------
# LOGOUT
def logout(request):
    auth.logout(request)
    return redirect('login')


# ------------------------------------------------------
# REGISTER
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']   # Teacher or Student

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password1,
                    email=email
                )
                Profile.objects.create(user=user, role=role)
                messages.success(request, 'User created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'register.html')


# ------------------------------------------------------
# TEACHER DASHBOARD — Create Assignments
@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        return redirect('student_dashboard')

    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        language = request.POST['language']
        deadline = request.POST.get('deadline')

        Assignment.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            language=language,
            deadline=deadline
        )
        messages.success(request, "✅ Assignment Created Successfully!")

    assignments = Assignment.objects.filter(teacher=request.user).order_by('-id')
    return render(request, 'teacher_dashboard.html', {
        'assignments': assignments,
        'now': timezone.now()
    })


# ------------------------------------------------------
# STUDENT DASHBOARD — View Assignments + Submissions
@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')

    assignments = Assignment.objects.all().order_by('-deadline')
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {
        'assignments': assignments,
        'submissions': submissions
    })


# ------------------------------------------------------
# CODE EXECUTION (Python / C++ / Java)
def execute_code(code, language):
    """Run Python, C++, or Java code and return stdout + stderr."""
    stdout, stderr = "", ""
    try:
        if language == "python":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
                temp.write(code.encode())
                temp.flush()
                result = subprocess.run(
                    ["python", temp.name],
                    capture_output=True, text=True, timeout=5
                )
                stdout, stderr = result.stdout, result.stderr

        elif language == "cpp":
            with tempfile.TemporaryDirectory() as tmpdir:
                cpp_file = os.path.join(tmpdir, "program.cpp")
                exe_file = os.path.join(tmpdir, "program.exe")
                with open(cpp_file, "w") as f:
                    f.write(code)
                compile_result = subprocess.run(
                    ["g++", cpp_file, "-o", exe_file],
                    capture_output=True, text=True
                )
                if compile_result.returncode != 0:
                    stderr = compile_result.stderr
                else:
                    run_result = subprocess.run(
                        [exe_file], capture_output=True, text=True, timeout=5
                    )
                    stdout, stderr = run_result.stdout, run_result.stderr

        elif language == "java":
            with tempfile.TemporaryDirectory() as tmpdir:
                java_file = os.path.join(tmpdir, "Main.java")
                with open(java_file, "w") as f:
                    f.write(code)
                compile_result = subprocess.run(
                    ["javac", java_file],
                    capture_output=True, text=True, cwd=tmpdir
                )
                if compile_result.returncode != 0:
                    stderr = compile_result.stderr
                else:
                    run_result = subprocess.run(
                        ["java", "Main"],
                        capture_output=True, text=True, timeout=5, cwd=tmpdir
                    )
                    stdout, stderr = run_result.stdout, run_result.stderr

    except Exception as e:
        stderr = str(e)
    return stdout, stderr


# ------------------------------------------------------
# SUBMIT ASSIGNMENT (with Run and Late Submission)
@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    stdout, stderr = None, None

    if request.method == "POST":
        code = request.POST['code']
        action = request.POST.get("action")  # run / submit
        current_time = timezone.now()

        # Run code
        stdout, stderr = execute_code(code, assignment.language)

        # Check for late submission
        is_late = current_time > assignment.deadline
        if is_late:
            messages.warning(request, "⚠️ You submitted after the deadline.")

        # Save only if submitted
        if action == "submit":
            Submission.objects.create(
                assignment=assignment,
                student=request.user,
                code=code,
                output=stdout,
                errors=stderr,
                is_late=is_late
            )
            messages.success(request, "✅ Submission saved successfully!")
            return redirect("student_dashboard")

    return render(request, 'submit_assignment.html', {
        'assignment': assignment,
        'stdout': stdout,
        'stderr': stderr
    })


# ------------------------------------------------------
# TEACHER REVIEWS SUBMISSIONS
@login_required
def review_submissions(request, assignment_id):
    if request.user.profile.role != 'teacher':
        return redirect('student_dashboard')

    submissions = Submission.objects.filter(
        assignment_id=assignment_id
    ).order_by('submitted_at')

    if request.method == "POST":
        sub_id = request.POST['sub_id']
        marks = request.POST['marks']
        feedback = request.POST['feedback']

        submission = Submission.objects.get(id=sub_id)
        submission.marks = marks
        submission.feedback = feedback
        submission.save()
        messages.success(request, "Feedback saved successfully!")

    return render(request, 'review_submissions.html', {'submissions': submissions})
