from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'admin2024'  # Your MySQL password
app.config['MYSQL_DB'] = 'student_dbms'  # Your MySQL database name

mysql = MySQL(app)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # Render the main interface

# Route for the interface page
@app.route('/interface')
def interface():
    return render_template('interface.html')  # Render the interface page

# Route to add a new student (GET and POST)
@app.route('/add_student.html', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Handle form submission
        student_id = request.form['studentId']
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO students (student_id, name, age, address, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (student_id, name, age, address, email, phone)

        cursor.execute(sql, values)
        mysql.connection.commit()
        cursor.close()

        

    return render_template('add_student.html')  # Render the add student page

# Route to view all students
@app.route('/view_students.html', methods=['GET'])
def view_students():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM students"
    cursor.execute(sql)
    students = cursor.fetchall()
    cursor.close()

    return render_template('view_students.html', students=students)  # Render all students


@app.route('/update_student', methods=['POST'])
def update_student():
    # Get data from the form
    student_id = request.form['studentId']  # ID of the student to be updated
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    cursor = mysql.connection.cursor()
    sql = "UPDATE students SET name = %s, age = %s, address = %s, email = %s, phone = %s WHERE student_id = %s"
    values = (name, age, address, email, phone, student_id)

    try:
        cursor.execute(sql, values)
        mysql.connection.commit()  # Commit the changes
    except Exception as e:
        mysql.connection.rollback()  # Roll back in case of error
        print(f"Error updating student: {e}")
        return "An error occurred while updating the student.", 500
    finally:
        cursor.close()  # Close the database cursor

    return redirect(url_for('view_students'))  # Redirect to a page showing all students# Handle cases where no student ID is provided
# Route to delete a student
@app.route('/delete_student.html', methods=['POST'])
def delete_student():
    student_id = request.form['studentId']

    cursor = mysql.connection.cursor()
    sql = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(sql, (student_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('view_students'))  # Redirect to view all students

# Route to search for a student
@app.route('/search_student.html', methods=['GET'])
def search_student():
    student_id = request.args.get('studentId')

    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM students WHERE student_id = %s"
    cursor.execute(sql, (student_id,))
    student = cursor.fetchone()
    cursor.close()

    return render_template('student_detail.html', student=student)  # Render student detail

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)