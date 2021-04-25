from django.http import HttpResponse
from django.template import loader
import mysql.connector
from django.views.decorators.csrf import csrf_exempt

def index(request):

    return HttpResponse("Welcome to the University Database.\nPlease log in:")

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
            host = "localhost",
            user = "root",
            passwd = "root",
            auth_plugin = "mysql_native_password",
            database = "university",
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

    data='<title>Student Info</title>'
    data='<h1>Courses:</h1>'
    data += '<table style="width:800px">'
    data += '<tr><th>Course ID</th> <th>Course Title</th>' + \
            '<th>Department Name</th> <th>Section</th>' + \
            '<th>Semester</th> <th>Year</th></tr>'
    for (course_id, sec_id, title, dept_name, semester, year) in mycursor:
        r = ('<tr>' + \
                '<th>' + str(course_id) + '</th>' + \
                '<th>' + title + '</th>' + \
                '<th>' + dept_name + '</th>' + \
                '<th>' + str(sec_id) + '</th>' + \
                '<th>' + str(semester) + '</th>' + \
                '<th>' + str(year) + '</th>' + \
                '</t>')
        data += r
    data += '</table>'

    mycursor.close()
    mydb.close()

    return HttpResponse(data)