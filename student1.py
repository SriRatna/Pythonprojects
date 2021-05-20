#Flask backend application to perform basic CRUD operations
#used Postman tool for API testing

from flask import Flask, jsonify, request
import psycopg2

#conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1', port='5432')

app = Flask(__name__)

#below code inserts new records, student id is primary key
@app.route('/home/insertnew', methods=['POST'])
def newstudent():
    conn = None
    message = {}
    form = request.get_json()
    try:
        conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute("insert into studentdetails (student_id, student_name, course_enrolled, phone, email) values(%s,%s,%s,%s,%s)",
                (form['id'], form['name'], form['course_enrolled'], form['phone'], form['email']))
        conn.commit()
        cur.close()
        message = {"message": "record inserted successfully"}
    except (Exception, psycopg2.DatabaseError) as error:
        message = {"message": "there is an error"}
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return jsonify(message)

#below code will fetch a single record from student table
@app.route('/home/fetchone')
def fetchone():
    conn = None
    message = {}
    sql = "select * from studentdetails where student_id = %s"
    form = request.get_json()
    try:
        conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1',
                                port='5432')
        cur = conn.cursor()
        cur.execute(sql, (form['id'],))
        rows = cur.fetchone()
        cur.close()
        if rows:
            message = {"record": rows}
        else:
            message = {"record": "no record found for this student id"}
    except (Exception, psycopg2.DatabaseError) as error:
        message = {"message": "there is an error"}
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return jsonify(message)

#below code will fetch all records from student table
@app.route('/home/fetchall')
def fetchall():
    conn = None
    message = {}
    sql = "select * from studentdetails"
    try:
        conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1',
                                port='5432')
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        if rows:
            message = {"record": rows}
        else:
            message = {"record": "no student records found"}
    except (Exception, psycopg2.DatabaseError) as error:
        message = {"message": "there is an error"}
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return jsonify(message)

#update a single record with id
@app.route('/home/update', methods=['PUT'])
def updatestudent():
    conn = None
    message = {}
    update_count = 0
    sql = "update studentdetails set student_name = %s,course_enrolled = %s,phone=%s,email=%s where student_id=%s"
    form = request.get_json()
    try:
        conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute(sql, (form['name'], form['course_enrolled'], form['phone'], form['email'], form['id']))
        update_count = cur.rowcount
        print("rows updated is", update_count)
        conn.commit()
        cur.close()
        if update_count > 0:
            message = {"message": "record updated successfully"}
        else:
            message = {"message": "no records found with the id"}
    except (Exception, psycopg2.DatabaseError) as error:
        message = {"message": "there is an error while updating the record"}
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return jsonify(message)

#delete a single reccord with student id provided
@app.route('/home/delete', methods=['DELETE'])
def deletestudent():
    conn = None
    message = {}
    del_count = 0
    sql = "delete from studentdetails where student_id=%s"
    form = request.get_json()
    try:
        conn = psycopg2.connect(database='studentdb', user='postgres', password='xx', host='127.0.0.1', port='5432')
        cur = conn.cursor()
        cur.execute(sql, (form['id'],))
        del_count = cur.rowcount
        print("rowcount in delete is", del_count)
        conn.commit()
        cur.close()
        if del_count > 0:
            message = {"message": "record deleted successfully"}
        else:
            message = {"message": "no record found for this id"}
    except (Exception, psycopg2.DatabaseError) as error:
        message = {"message": "there is an error while deleting the record"}
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return jsonify(message)

if __name__ == "__main__":
    app.run(debug = True, port=4990)


