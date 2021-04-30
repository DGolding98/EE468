from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import mysql.connector
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@login_required
def professor(request):

    if not (request.user.username == 'instructor' or request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)

    form = '<!DOCTYPE html>' + \
        '<html>' + \
        '<body>' + \
        '<h1>Professor:</h1>' + \
        '<form action="courses/" method="post">' + \
            '<input type-"text" id="course_id" name="course_id">' + \
            '<label for="course_id"> Course ID</label><br>' + \
            '<input type-"text" id="sec_id" name="sec_id">' + \
            '<label for="sec_id"> Section</label><br>' + \
            '<input type="submit" value = "View courses">' + \
        '</form><br><br>' + \
        '<form action="students/" method="post">' + \
            '<input type-"text" id="instructor_name" name="instructor_name">' + \
            '<label for="instructor_name"> Instructor Last Name</label><br>' + \
            '<input type-"text" id="semester" name="semester">' + \
            '<label for="semester"> Semester [1 for fall, 2 for spring]</label><br>' + \
            '<input type-"text" id="year" name="year">' + \
            '<label for="year"> Year [XXXX]</label><br>' + \
            '<input type="submit" value="View students">' + \
        '</form>' + \
        '<p>Choose what to do.</p>' + \
        '<p><a href="/">Home</a></p>' + \
        '<p><a href="/accounts/login/">Log Out</a></p>' + \
        '</body>' + \
        '</html>'

    return HttpResponse(form)

@login_required
@csrf_exempt
def professorCourses(request):
    if not (request.user.username == 'instructor' or request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # passwd="root",
        passwd="ledzepp56",
        auth_plugin="mysql_native_password",
        database="university",
    )

    mycursor = mydb.cursor()

    course_id = request.POST['course_id']
    section = request.POST['sec_id']
    query = "select course_id, section, count(course_id) from" \
            " (select course.course_id as course_id, takes.id as student_id, takes.sec_id as section from " \
            "course join takes where course.course_id=takes.course_id) as courses" \

    if course_id != "":
        query += " where course_id=\"" + course_id + "\""
    if section != "":
        if course_id != "":
            query += " and section=" + section
        else:
            query += " where section=" + section
    query += " group by course_id, section;"
    mycursor.execute(query)

    data = '<h1>Courses:</h1>'
    data += '<table style="width:800px">'
    data += '<tr><th>Course ID</th> <th>Section ID</th> <th>Number of Students</th></tr>'
    for (course_id, sec_id, count) in mycursor:
        r = ('<tr>' +
             '<th>' + str(course_id) + '</th>' +
             '<th>' + str(sec_id) + '</th>' +
             '<th>' + str(count) + '</th>' +
             '</t>')
        data += r
    data += '</table>'
    data += '<a href="/professor/">Back</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)

@login_required
@csrf_exempt
def professorStudents(request):
    if not (request.user.username == 'instructor' or request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # passwd="root",
        passwd="ledzepp56",
        auth_plugin="mysql_native_password",
        database="university",
    )

    mycursor = mydb.cursor()

    instructor = request.POST['instructor_name']
    semester = request.POST['semester']
    year = request.POST['year']
    query = "select courses.course_id course_id, courses.sec_id sec_id, courses.semester semester, courses.year year," \
            " courses.name name, teaches.id teacher_id, instructor.name instructor from teaches join instructor" \
            " join (select student.name name, course_id, sec_id, semester, year from student join takes" \
            " where student.id=takes.id) as courses where courses.course_id=teaches.course_id" \
            " and courses.semester=teaches.semester and courses.year=teaches.year and courses.sec_id=teaches.sec_id" \
            " and teaches.id=instructor.ID"

    if instructor != "":
        query += " and instructor.name=\"" + instructor + "\""
    if semester != "":
        query += " and courses.semester=" + semester
    if year != "":
        query += " and courses.year=" + year
    query += ";"
    mycursor.execute(query)

    data = '<h1>Students:</h1>'
    data += '<table style="width:800px">'
    data += '<tr><th>Course ID</th> <th>Section ID</th> <th>Student Name</th>' + \
            '<th>Semester</th> <th>Year</th> <th>Instructor ID</th> <th>Instructor</th></tr>'
    for (course_id, sec_id, semester, year, name, teacher_id, instructor) in mycursor:
        r = ('<tr>' +
             '<th>' + str(course_id) + '</th>' +
             '<th>' + str(sec_id) + '</th>' +
             '<th>' + str(name) + '</th>' +
             '<th>' + str(semester) + '</th>' +
             '<th>' + str(year) + '</th>' +
             '<th>' + str(teacher_id) + '</th>' +
             '<th>' + str(instructor) + '</th>' +
             '</t>')
        data += r
    data += '</table>'
    data += '<a href="/professor/">Back</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)

@csrf_exempt
@login_required
def student(request):
    if not (request.user.username == 'student' or request.user.username == 'instructor' or request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)

    form = '<!DOCTYPE html>' + \
           '<html>' + \
           '<body>' + \
           '<h1>Display Courses</h1>' + \
           '<form action="studentResult/" method="post">' + \
           '<input type-"text" id="department" name="department">' + \
           '<label for="department"> Department</label><br><br>' + \
           '<input type-"text" id="semester" name="semester">' + \
           '<label for="semester"> Semester [1 for fall, 2 for spring]</label><br><br>' + \
           '<input type-"text" id="year" name="year">' + \
           '<label for="year"> Year [XXXX]</label><br><br>' + \
           '<input type="submit" value = "Submit">' + \
           '</form>' + \
           '<p>Click on the submit button to submit the form.</p>' + \
           '<p><a href="/">Home</a></p>' + \
           '<p><a href="/accounts/login/">Log Out</a></p>' + \
           '</html>'


    return HttpResponse(form)

@login_required
@csrf_exempt
def studentResult(request):
    if not (request.user.username == 'student' or request.user.username == 'instructor' or request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # passwd="root",
        passwd="ledzepp56",
        auth_plugin="mysql_native_password",
        database="university",
    )

    mycursor = mydb.cursor()

    department = request.POST['department']
    semester = request.POST['semester']
    year = request.POST['year']
    query = "select course.course_id, title, dept_name, sec_id, semester, year from course join teaches " + \
            "where course.course_id=teaches.course_id"
    if department != "":
        query += " and dept_name=\"" + department + "\""
    if semester != "":
        query += " and semester=\"" + semester + "\""
    if year != "":
        query += " and year=\"" + year + "\""
    query += ";"
    mycursor.execute(query)

    data = '<h1>Courses:</h1>'
    data += '<table style="width:800px">'
    data += '<tr><th>Course ID</th> <th>Course Title</th>' + \
            '<th>Department Name</th> <th>Section</th>' + \
            '<th>Semester</th> <th>Year</th></tr>'
    for (course_id, sec_id, title, dept_name, semester, year) in mycursor:
        r = ('<tr>' +
             '<th>' + str(course_id) + '</th>' +
             '<th>' + str(title) + '</th>' +
             '<th>' + str(dept_name) + '</th>' +
             '<th>' + str(sec_id) + '</th>' +
             '<th>' + str(semester) + '</th>' +
             '<th>' + str(year) + '</th>' +
             '</t>')
        data += r
    data += '</table>'
    data += '<a href="/student/">Back</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)

@login_required
def administrator(request):
    if not (request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)

    form = '<!DOCTYPE html>' + \
        '<html>' + \
        '<body>' + \
        '<h1>Administrator:</h1>' + \
        '<h3> Choose which following Functions to perform: </h3>' + \
        '<form action="f1/" method="post">' + \
            '<p> F1. Create a list of professors sorted by: <p>' + \
            '<INPUT TYPE=radio NAME="sort_method" VALUE="name" CHECKED> Name</LABEL><BR>' + \
            '<INPUT TYPE=radio NAME="sort_method" VALUE="dept"> Department</LABEL><BR>' + \
            '<INPUT TYPE=radio NAME="sort_method" VALUE="salary"> Salary</LABEL>' + \
            '<p> </p>' + \
            '<input type="submit" value = "View professors">' + \
        '</form><br><br>' + \
        '<form action="f2/" method="post">' + \
            '<p> F2. Create a table of the min/max/average salaries of a department: <p>' + \
            '<input type-"text" id="department" name="department"><br><br>' + \
            '<input type="submit" value = "View salaries">' + \
        '</form><br><br>' + \
        '<form action="f3/" method="post">' + \
            '<p> F3. Create a table of professors, their department and how many students they taught in a given semester: <p>' + \
            '<input type-"text" id="semester" name="semester"><br><br>' + \
            '<input type="submit" value = "View professors">' + \
        '</form>' + \
        '<p>Choose a function above.</p>' + \
        '<p><a href="/">Home</a></p>' + \
        '<p><a href="/accounts/login/">Log Out</a></p>' + \
        '</body>' + \
        '</html>'

    return HttpResponse(form)

@login_required
@csrf_exempt
def f1(request):
    if not (request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            # passwd="root",
            passwd="ledzepp56",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    
    mycursor = mydb.cursor()

    sort_method = request.POST['sort_method']
    query = "select * from instructor"
    query += " order by " + sort_method 
    query += ";"
    mycursor.execute(query)

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    data += '<tr><th>ID</th> <th>Name</th> <th>Dept</th> <th>Salary</th> </tr>'
    for (ID, name, dept, salary) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(ID) + '</th>' + \
                '<th>' + str(name) + '</th>' + \
                '<th>' + str(dept) + '</th>' + \
                '<th>' + str(salary) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'
    data += '<a href="/admin/">Back</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)

@login_required
@csrf_exempt
def f2(request):
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            # passwd="root",
            passwd="ledzepp56",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    mycursor = mydb.cursor()
    dept = request.POST['department']
    query = "select MAX(salary), MIN(salary), AVG(salary)" + \
    " from instructor " + \
    "where instructor.dept_name = \"" + dept + "\";"
    mycursor.execute(query) 

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    data += '<tr><th>Max</th> <th>Min</th> <th>Average</th></tr>'
    for (max, min, avg) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(max) + '</th>' + \
                '<th>' + str(min) + '</th>' + \
                '<th>' + str(avg) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'
    data += '<a href="/admin/">Back</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)

@login_required
@csrf_exempt
def f3(request):
    if not (request.user.username == 'admin'):
        return redirect('/login/?next=%s' % request.path)
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            # passwd="root",
            passwd="ledzepp56",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    
    mycursor = mydb.cursor()

    semester = request.POST['semester']
    query = "select I.name, I.dept_name, COUNT(S.name) " + \
    "from instructor I, student S, teaches T, takes R " + \
    "where I.ID = T.id AND T.course_id = R.course_id AND R.id = S.ID "
    if semester != "":
        query += "and R.semester = "  + semester 
        query += ";"
    mycursor.execute(query)

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    data += '<tr><th>Name</th> <th>Dept</th> <th>Number of Students</th> </tr>'
    for (name, dept, count) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(name) + '</th>' + \
                '<th>' + str(dept) + '</th>' + \
                '<th>' + str(count) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'
    data += '<a href="/admin/">Back</a>'

    # data += '<a href="/">Home</a>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)
