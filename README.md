# Academic Management System

## Overview

The Academic Management System is a web-based application built using Python Flask and MySQL.
It helps manage different academic operations such as student records, faculty details, course management, attendance tracking, examination details, and results.

This system allows administrators to efficiently manage academic information through a simple web interface.

---

## Features

* Admin login system
* Student management
* Faculty management
* Department management
* Course management
* Enrollment management
* Attendance tracking
* Examination management
* Result management
* Dashboard for navigation

---

## Technologies Used

Backend:

* Python
* Flask

Frontend:

* HTML
* CSS

Database:

* MySQL

Tools:

* VS Code
* MySQL Workbench

---

## Project Structure

```
APP
│
├── app.py
├── appppp.mwb
│
└── templates
    ├── index.html
    ├── login.html
    ├── students.html
    ├── faculty.html
    ├── department.html
    ├── course.html
    ├── enrollment.html
    ├── attendance.html
    ├── examination.html
    └── results.html
```

---

## Database

Database Name:

```
college_db
```

Connection configuration inside `app.py`:

```
host="localhost"
user="root"
password="root"
database="college_db"
```

You can modify these values according to your MySQL setup.

---

## Installation

### 1 Clone the Repository

```
git clone https://github.com/yourusername/academic-management-system.git
```

### 2 Navigate to the project

```
cd academic-management-system
```

### 3 Install dependencies

```
pip install -r requirements.txt
```

### 4 Run the application

```
python app.py
```

### 5 Open browser

```
http://127.0.0.1:5000
```

---

## Future Improvements

* Role based login (Admin / Faculty / Student)
* Student portal
* Attendance analytics
* Marks visualization
* API integration
* Better UI using Bootstrap

---

## Author

Developed by **Jaishanth Lenin**
Academic Project – Computer Science
