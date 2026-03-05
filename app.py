from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "cse"

# -------------------- DATABASE CONNECTION --------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # your MySQL password
        database="college_db"
    )

# -------------------- ROOT REDIRECT --------------------
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:  # already logged in
        return redirect(url_for('dashboard'))

    error = None  # variable to store error message

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE Username=%s AND Password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['username'] = user['Username']
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Username or Password"  # set error message

    return render_template('login.html', error=error)


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

# -------------------- DEPARTMENT --------------------
@app.route('/department', methods=['GET', 'POST'])
def department():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['deptname']
        loc = request.form['location']
        cursor.execute("INSERT INTO Department (DeptName, Location) VALUES (%s, %s)", (name, loc))
        db.commit()
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('department.html', departments=departments)

# -------------------- STUDENT --------------------
@app.route('/student', methods=['GET', 'POST'])
def student():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        dept_id = request.form['departmentid']
        cursor.execute(
            "INSERT INTO Student (Name, DOB, Email, Phone, DepartmentID) VALUES (%s, %s, %s, %s, %s)",
            (name, dob, email, phone, dept_id)
        )
        db.commit()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('students.html', students=students, departments=departments)

# -------------------- FACULTY --------------------
@app.route('/faculty', methods=['GET', 'POST'])
def faculty():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dept_id = request.form['department']
        cursor.execute(
            "INSERT INTO Faculty (Name, Email, Phone, DepartmentID) VALUES (%s, %s, %s, %s)",
            (name, email, phone, dept_id)
        )
        db.commit()

    cursor.execute("""SELECT f.FacultyID, f.Name, f.Email, f.Phone, d.DeptName
                      FROM Faculty f LEFT JOIN Department d ON f.DepartmentID = d.DepartmentID""")
    faculties = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('faculty.html', faculties=faculties, departments=departments)

# -------------------- COURSE --------------------
@app.route('/course', methods=['GET', 'POST'])
def course():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Department")
    departments = cursor.fetchall()
    cursor.execute("SELECT * FROM Faculty")
    faculties = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['coursename']
        credits = request.form['credits']
        dept_id = request.form['department']
        fac_id = request.form['faculty']
        cursor.execute(
            "INSERT INTO Course (CourseName, Credits, DepartmentID, FacultyID) VALUES (%s, %s, %s, %s)",
            (name, credits, dept_id, fac_id)
        )
        db.commit()

    cursor.execute("""SELECT c.CourseID, c.CourseName, c.Credits, d.DeptName, f.Name as FacultyName
                      FROM Course c
                      LEFT JOIN Department d ON c.DepartmentID=d.DepartmentID
                      LEFT JOIN Faculty f ON c.FacultyID=f.FacultyID""")
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('course.html', courses=courses, departments=departments, faculties=faculties)

# -------------------- ENROLLMENT --------------------
@app.route('/enrollment', methods=['GET', 'POST'])
def enrollment():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()

    if request.method == 'POST':
        student_id = request.form['student']
        course_id = request.form['course']
        date = request.form['date']
        cursor.execute(
            "INSERT INTO Enrollment (StudentID, CourseID, EnrollmentDate) VALUES (%s, %s, %s)",
            (student_id, course_id, date)
        )
        db.commit()

    cursor.execute("""SELECT e.EnrollmentID, s.Name as StudentName, c.CourseName, e.EnrollmentDate
                      FROM Enrollment e
                      LEFT JOIN Student s ON e.StudentID=s.StudentID
                      LEFT JOIN Course c ON e.CourseID=c.CourseID""")
    enrollments = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('enrollment.html', students=students, courses=courses, enrollments=enrollments)

# -------------------- ATTENDANCE --------------------
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""SELECT e.EnrollmentID, s.Name as StudentName, c.CourseName
                      FROM Enrollment e
                      LEFT JOIN Student s ON e.StudentID=s.StudentID
                      LEFT JOIN Course c ON e.CourseID=c.CourseID""")
    enrollments = cursor.fetchall()

    if request.method == 'POST':
        enrollment_id = request.form['enrollment']
        date = request.form['date']
        status = request.form['status']
        cursor.execute(
            "INSERT INTO Attendance (EnrollmentID, Date, Status) VALUES (%s, %s, %s)",
            (enrollment_id, date, status)
        )
        db.commit()

    cursor.execute("""SELECT a.AttendanceID, s.Name as StudentName, c.CourseName, a.Date, a.Status
                      FROM Attendance a
                      LEFT JOIN Enrollment e ON a.EnrollmentID=e.EnrollmentID
                      LEFT JOIN Student s ON e.StudentID=s.StudentID
                      LEFT JOIN Course c ON e.CourseID=c.CourseID""")
    attendance = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('attendance.html', enrollments=enrollments, attendance=attendance)

# -------------------- EXAMINATION --------------------
@app.route('/examination', methods=['GET', 'POST'])
def examination():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()

    if request.method == 'POST':
        course_id = request.form['course']
        date = request.form['date']
        exam_type = request.form['examtype']
        cursor.execute(
            "INSERT INTO Examination (CourseID, ExamDate, ExamType) VALUES (%s, %s, %s)",
            (course_id, date, exam_type)
        )
        db.commit()

    cursor.execute("""SELECT ex.ExamID, c.CourseName, ex.ExamDate, ex.ExamType
                      FROM Examination ex
                      LEFT JOIN Course c ON ex.CourseID=c.CourseID""")
    exams = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('examination.html', courses=courses, exams=exams)

# -------------------- RESULTS --------------------
@app.route('/results', methods=['GET','POST'])
def results():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Fetch exams with course name
    cursor.execute("""
        SELECT ex.ExamID, c.CourseName, ex.ExamType
        FROM Examination ex
        LEFT JOIN Course c ON ex.CourseID = c.CourseID
    """)
    exams = cursor.fetchall()

    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()

    if request.method == 'POST':
        exam = request.form['exam']
        student = request.form['student']
        marks = request.form['marks']
        grade = request.form['grade']
        cursor.execute(
            "INSERT INTO Results (ExamID, StudentID, Marks, Grade) VALUES (%s,%s,%s,%s)",
            (exam, student, marks, grade)
        )
        db.commit()

    # Fetch results with course and student names
    cursor.execute("""
        SELECT r.ResultID, s.Name as StudentName, c.CourseName, ex.ExamType, r.Marks, r.Grade
        FROM Results r
        LEFT JOIN Examination ex ON r.ExamID = ex.ExamID
        LEFT JOIN Course c ON ex.CourseID = c.CourseID
        LEFT JOIN Student s ON r.StudentID = s.StudentID
    """)
    results = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('results.html', exams=exams, students=students, results=results)

# -------------------- RUN --------------------
if __name__ == '__main__':
    app.run(debug=True)
