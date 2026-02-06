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


## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend Framework** | Django 4.2+ |
| **Frontend Framework** | Bootstrap 5 |
| **Programming Language** | Python 3.8+ |
| **Database** | PostgreSQL (Production) |
| **Authentication** | Django Authentication System |
| **Code Execution** | Python Subprocess, JDK, G++ |

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


# PostgreSQL DATABASE ---- Setup for Django Project

This README provides a step-by-step guide to set up **PostgreSQL** with a **Django** project.

---

## Prerequisites

* Python 3.x installed
* Django project already created
* Internet connection

---

## Step 1: Download PostgreSQL

Download PostgreSQL from the official website:

👉 [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

---

## Step 2: Install PostgreSQL

* Run the installer
* Set a **password** for the PostgreSQL superuser (`postgres`)
* Keep the **default port number: 5432**
* Complete the installation

⚠️ **Important:** Remember the password. It will be used later in pgAdmin and Django.

---

## Step 3: Download & Install pgAdmin 4

pgAdmin is a GUI tool to manage PostgreSQL databases.

* Download pgAdmin 4 from the PostgreSQL website
* Install and open pgAdmin

---

## Step 4: Connect PostgreSQL in pgAdmin

* Open **pgAdmin 4**
* When prompted, enter the **same password** you set during PostgreSQL installation

---

## Step 5: Create a Database

1. In pgAdmin, expand **Servers → PostgreSQL**
2. Right-click on **Databases**
3. Click **Create → Database**
4. Enter a database name (example: `myproject_db`)
5. Click **Save**

---

## Step 6: Install PostgreSQL Adapter for Python

Install `psycopg2`, which acts as a connector between **PostgreSQL and Python**:

```bash
pip install psycopg2
```

(You may also use `psycopg2-binary` if required.)

---

## Step 7: Configure Django Database Settings

Open `settings.py` in your Django project and update the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject_db',
        'USER': 'postgres',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Replace values according to your setup.

---

## Step 8: Apply Migrations

Run the following command to create tables in PostgreSQL:

```bash
python manage.py migrate
```

---

## ✅ Setup Complete

🎉 PostgreSQL is now successfully connected with your Django project.

You can now:

* Create models
* Run migrations
* Store data in PostgreSQL

---

## Troubleshooting Tips

* Make sure PostgreSQL service is running
* Double-check database name, password, and port
* Restart Django server if needed

---

**Happy Coding 🚀**


