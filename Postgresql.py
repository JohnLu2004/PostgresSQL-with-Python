import psycopg2
from psycopg2 import Error

def main():
    # Database info
    dbname = "Assignment3"
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        if conn:
            # Create database
            createStudentDatabase(conn)
            init(conn)
            print("Database created and filled successfully!")

            input_val = ""
            #while not wnting to exit, give them options
            while input_val != "0":
                print("Enter 0 to exit.")
                print("Enter 1 to get all students.")
                print("Enter 2 to add a student.")
                print("Enter 3 to update a student's email.")
                print("Enter 4 to delete a student.")
                input_val = input()
                if input_val == "1":
                    getAllStudents(conn)
                elif input_val == "2":
                    print("Enter the student's first name:")
                    first_name = input()
                    print("Enter the student's last name:")
                    last_name = input()
                    print("Enter the student's email:")
                    email = input()
                    print("Enter the student's enrollment date (YYYY-MM-DD):")
                    enrollment_date = input()
                    addStudent(conn, first_name, last_name, email, enrollment_date)
                elif input_val == "3":
                    print("Enter the student's ID:")
                    student_id = input()
                    print("Enter the student's new email:")
                    new_email = input()
                    updateStudentEmail(conn, student_id, new_email)
                elif input_val == "4":
                    print("Enter the student's ID:")
                    student_id = input()
                    deleteStudent(conn, student_id)
                    
            # delete all students and delete database
            deleteStudentDatabase(conn)
            conn.close()
        else:
            print("Failed to establish connection.")
    except Error as e:
        print(e)

#adds some students to the database
def init(conn):
    addStudent(conn, "John", "Doe", "john.doe@example.com", "2023-09-01")
    addStudent(conn, "Jane", "Smith", "jane.smith@example.com", "2023-09-01")
    addStudent(conn, "Jim", "Beam", "jim.beam@example.com", "2023-09-02")

#creates the student database
def createStudentDatabase(conn):
    try:
        # Create cursor
        cur = conn.cursor()
        # Execute SQL query
        cur.execute("""
            CREATE TABLE students (
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE
            )
        """)
        cur.close()
    except Error as e:
        print(e)

#deletes the student database
def deleteStudentDatabase(conn):
    try:
        # Create cursor
        cur = conn.cursor()
        # Execute SQL query
        cur.execute("DROP TABLE students")
        cur.close()
    except Error as e:
        print(e)

#gets all students from the database
def getAllStudents(conn):
    try:
        # Create cursor
        cur = conn.cursor()
        # Execute SQL query
        cur.execute("SELECT first_name, last_name, email, enrollment_date, student_id FROM students")
        # Fetch all rows
        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1], "with email", row[2], "who enrolled on", row[3], "with ID", row[4])
        cur.close()
    except Error as e:
        print(e)

#adds a student to the database
def addStudent(conn, first_name, last_name, email, enrollment_date):
    try:
        # Create cursor
        cur = conn.cursor()
        # INSERT Operation
        cur.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, email, enrollment_date))
        print("A new student was inserted successfully!")
        cur.close()
    except Error as e:
        print(e)

#updates a student's email
def updateStudentEmail(conn, student_id, new_email):
    try:
        # Create cursor
        cur = conn.cursor()
        # Update operation
        cur.execute("""
            UPDATE students
            SET email = %s
            WHERE student_id = %s
        """, (new_email, student_id))
        if cur.rowcount > 0:
            print("Email updated successfully for student with ID:", student_id)
        else:
            print("No student found with ID:", student_id)
        cur.close()
    except Error as e:
        print(e)

#deletes a student from the database
def deleteStudent(conn, student_id):
    try:
        # Create cursor
        cur = conn.cursor()
        # DELETE Operation
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        if cur.rowcount > 0:
            print("A student was deleted successfully!")
        else:
            print("No student found with ID:", student_id)
        cur.close()
    except Error as e:
        print(e)

if __name__ == "__main__":
    main()
