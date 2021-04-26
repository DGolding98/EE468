from django.http import HttpResponse
from django.template import loader
import mysql.connector
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Welcome to the University Database.\nPlease log in:")


def professor(request):
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
            '<input type-"text" id="courseID" name="courseID">' + \
            '<label for="courseID"> Course ID</label><br>' + \
            '<input type-"text" id="semester" name="semester">' + \
            '<label for="semester"> Semester [1 for fall, 2 for spring]</label><br>' + \
            '<input type-"text" id="year" name="year">' + \
            '<label for="year"> Year [XXXX]</label><br>' + \
            '<input type="submit" value="View students">' + \
        '</form>' + \
        '<p>Choose what to do.</p>' + \
        '</body>' + \
        '</html>'

    return HttpResponse(form)


@csrf_exempt
def professorCourses(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        auth_plugin="mysql_native_password",
        database="university",
    )

    mycursor = mydb.cursor()

    course_id = request.POST['course_id']
    section = request.POST['sec_id']
    query = "select C.course_id as course_id, C.sec_id as sec_id, count(C.course_id) as count " \
            "from (select course.course_id, takes.id, takes.sec_id from course join takes " \
            "where course.course_id=takes.course_id) C group by course_id, sec_id"
    if course_id != "":
        query += " and course_id=\"" + course_id + "\""
    if section != "":
        query += " and sec_id=\"" + section + "\""
    query += ";"
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

    mycursor.close()
    mydb.close()

    return HttpResponse(data)


@csrf_exempt
def professorStudents(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        auth_plugin="mysql_native_password",
        database="university",
    )

    mycursor = mydb.cursor()

    department = request.POST['courseID']
    semester = request.POST['semester']
    year = request.POST['year']
<<<<<<< HEAD
    query = "select takes.course_id as course_id, name, sec_id, takes.semester as semester, takes.year as year" + \
            " from student join takes where student.id=takes.id;"
    mycursor.execute(query)

    data = '<h1>Students:</h1>'
    data += '<table style="width:800px">'
    data += '<tr><th>Course ID</th> <th>Student name</th> <th>Section</th>' + \
            '<th>Semester</th> <th>Year</th></tr>'
    for (course_id, name, sec_id, semester, year) in mycursor:
        r = ('<tr>' +
             '<th>' + str(course_id) + '</th>' +
             '<th>' + str(name) + '</th>' +
             '<th>' + str(sec_id) + '</th>' +
             '<th>' + str(semester) + '</th>' +
             '<th>' + str(year) + '</th>' +
             '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)
=======
    return HttpResponse("Professor: View students")
>>>>>>> 6b285e002c9fc1915879454541bce91568b64686


def student(request):
    form = '<!DOCTYPE html>' + \
           '<html>' + \
           '<body>' + \
           '<h1>Display Courses</h1>' + \
           '<form action="studentResult/" method="post">' + \
           '<label for="department">Department </label>' + \
           '<input type-"text" id="department" name="department"><br><br>' + \
           '<label for="semester">Semester [1 for fall, 2 for spring] </label>' + \
           '<input type-"text" id="semester" name="semester"><br><br>' + \
           '<label for="year">Year [XXXX] </label>' + \
           '<input type-"text" id="year" name="year"><br><br>' + \
           '<input type="submit" value = "Submit">' + \
           '</form>' + \
           '<p>Click on the submit button to submit the form.</p>' + \
           '</body>' + \
           '</html>'

    return HttpResponse(form)


@csrf_exempt
def studentResult(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
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
             '<th>' + title + '</th>' +
             '<th>' + dept_name + '</th>' +
             '<th>' + str(sec_id) + '</th>' +
             '<th>' + str(semester) + '</th>' +
             '<th>' + str(year) + '</th>' +
             '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)


def administrator(request):
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
        '</body>' + \
        '</html>'

    return HttpResponse(form)


@csrf_exempt
def f1(request):
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "YES",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    
    mycursor = mydb.cursor()

    sort_method = request.POST['sort_method']
    query = "select * from instructor" + \
    " order by\"" + sort_method + "\";"
    mycursor.execute(query)

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    for (ID, name, dept, salary) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(ID) + '</th>' + \
                '<th>' + name + '</th>' + \
                '<th>' + dept + '</th>' + \
                '<th>' + str(salary) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)


@csrf_exempt
def f2(request):
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "YES",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    
    mycursor = mydb.cursor()

    department = request.POST['department']
    query = "select MAX(salary), MIN(salary), AVG(salary)" + \
    " from instructor"
    " where instructor.dept = \"" + department + "\";" + \
    mycursor.execute(query)

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    for (max, min, avg) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(max) + '</th>' + \
                '<th>' + str(min) + '</th>' + \
                '<th>' + str(avg) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)


@csrf_exempt
def f3(request):
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "YES",
            auth_plugin = "mysql_native_password",
            database = "university",
            )
    
    mycursor = mydb.cursor()

    semester = request.POST['semester']
    query = "select I.name, I.dept, COUNT(S.name)" + \
    "from instructor I, student S, teaches T, takes R" + \
    "where I.ID = T.id AND T.course_id = R.course_id AND R.id = S.ID" + \
    "and R.semester = \"" + semester + "\";" + \
    mycursor.execute(query)

    data='<title>Administrator Info</title>'
    data='<h1>Results:</h1>'
    data += '<table style="width:400px">'
    for (name, dept, count) in mycursor:
        r = ('<tr>' + \
                '<th>' + name + '</th>' + \
                '<th>' + dept + '</th>' + \
                '<th>' + str(COUNT(S.name)) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)