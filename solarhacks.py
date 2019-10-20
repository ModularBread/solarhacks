import sqlite3
from flask import Flask
from flask import request
from flask import g


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

            

app = Flask(__name__)

def get_db():
    if not hasattr(g, 'solarhacks.db'):
        g.conn = create_connection('solarhacks.db')
    return g.conn

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'solarhacks.db'):
        g.conn_db.close()
        

@app.route("/signupteacher", methods = ['POST'])
def signupteacher():
    conn = get_db()
    cur = conn.cursor()
    content = request.get_json()
    for key in content.keys():
        cur.execute('SELECT username FROM teacherusers WHERE username = ?', (key,))
        if cur.fetchone() != None:
            return "There is already an account with this username. Please try again"
        else:
            main(key, content[key], conn, 'teacher')

    
    
    return "success"
    
@app.route("/teachersignin", methods = ['POST'])
def signinteacher():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT pass FROM teacherusers WHERE username = ?', (key,))
        s_id = cur.fetchone()
        if s_id == None:
            return 'fail'
        elif s_id[0] == content[key]:
            return 'success'
        else:
            return 'fail'

@app.route("/signupstudent", methods = ['POST'])
def signupstudent():
    conn = get_db()
    cur = conn.cursor()
    content = request.get_json()
    for key in content.keys():
        cur.execute('SELECT username FROM studentusers WHERE username = ?', (key,))
        if cur.fetchone() != None:
            return "There is already an account with this username. Please try again"
        else:
            main(key, content[key], conn, 'student')

    
    
    return "success"
    
@app.route("/studentsignin", methods = ['POST'])
def signinstudent():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT pass FROM studentusers WHERE username = ?', (key,))
        s_id = cur.fetchone()
        if s_id == None:
            return 'fail'
        elif s_id[0] == content[key]:
            return 'success'
        else:
            return 'fail'


@app.route("/getstudents", methods = ['POST'])
def getstudents():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT student FROM teacherstudents WHERE teacher = ?', (content[key],))
    s_id = cur.fetchone()
    if s_id == None:
        return ''
    else:
        return s_id


@app.route("/addassignments", methods = ['POST'])
def addassignment():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        teacher = key
        question = content[key].split(',')[0]
        answer = content[key].split(',')[1]
        cur.execute('DELETE FROM questions WHERE teacher = ?', (teacher,))
        cur.execute('INSERT INTO questions(teacher,question,answer) VALUES(?,?,?)', (teacher, question, answer,))
        return ""
@app.route("/lessonplan", methods = ['POST'])
def lasttopic():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('DELETE FROM khan WHERE teacher = ?', (teacher,))
        cur.execute('INSERT INTO khan(teacher,url) VALUES(?,?)', (key, content[key],))
    





@app.route("/addteachers", methods = ['POST'])
def addteachers():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('INSERT INTO teacherstudents(teacher,student) VALUES(?,?)', (content[key], key,))
        print(content[key])
        print(key)
    return 'success'
    


@app.route("/getteachers", methods = ['POST'])        
def getteachers():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT ? FROM teacherstudents WHERE student = ?', (content[key], 'teacher',))
        s_id = cur.fetchone()
        if s_id == None:
            return ""
        else:
            return s_id

@app.route("/getassignment", methods = ['POST'])
def getassignment():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT question FROM questions WHERE teacher = ?',(content[key],))
        return cur.fetchone()[0]

@app.route("/checkassignment", methods = ['POST'])
def checkassignment():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        teacher = key;
        question = content[key]
        cur.execute('SELECT answer FROM questions WHERE teacher = ? and question = ?', (teacher,question,))
        if cur.fetchone()[0] == answer:
            return 'correct'
        else:
            return 'incorrect'

@app.route("/getlesson", methods = ['POST'])
def getlesson():
    content = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for key in content.keys():
        cur.execute('SELECT url FROM khan WHERE teacher = ?',(content[key],))











def create_userteacher(user, conn, db):


    sql = ''' INSERT INTO teacherusers(username,pass)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)

    ret = cur.lastrowid
    return ret

def create_userstudent(user, conn, db):


    sql = ''' INSERT INTO studentusers(username,pass)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)

    ret = cur.lastrowid
    return ret



def main(username, password, conn, db):
    with conn:
        user = (username, password);
        if db == 'teacher':
            user_id = create_userteacher(user, conn, db)
        elif db == 'student':
            user_id = create_userstudent(user,conn, db)

    conn.close()


if __name__ == "__main__":
    app.run(host='10.10.148.51')


        
