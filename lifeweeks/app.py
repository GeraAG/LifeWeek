from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

current_age = 1571


@app.route("/")
def home():
    database = 'lifeweeks'
    conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")

    table_exists_users = table_exists(conn, database, 'users')
    user_id = '1'
    user = ()
    current_age = 1571
    if table_exists_users:
        user = getUserID(conn, 'users')
        user_id = str(user[0])
        #current_age = getAgeInWeeks(user[2])
        user_name = user[1]

    table_name = 'life'
    table_exists_life = table_exists(conn, database, table_name)

    table_is_full = False
    if table_exists_life:
        table_is_full = check_table_is_full(conn, user_id, table_name)

    if table_exists_life and not table_is_full:
        print('does not exist')
        #populate_table_all(conn, table_name, user_id)

    if conn:
        conn.close()

    return render_template('index.html', title=user_name, age=current_age)

@app.route("/note", methods=['GET', 'POST'])
def note():
    if request.method == 'GET':
        database = 'lifeweeks'
        conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")
        user_id = '1'
        week_id = request.args.get('week_id')

        note = getNote(conn, week_id, user_id)
        if note == None:
            note = ''

        if conn:
            conn.close()
        return render_template('note.html', note=note, week=week_id)

    if request.method == 'POST':
        database = 'lifeweeks'
        conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")
        user_id = '1'
        data = request.get_json(force=True)
        newNote = data['text']
        week_id = data['week_id']
        print(week_id)

        changeNote(conn, user_id, week_id, newNote)

        if conn:
            conn.close()

        return 'Success'

def table_exists(con, database, table):
    exists = False
    try:
        cursor = con.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_catalog='" + database + "' AND table_schema='public'AND table_name='" + table +"');")
        exists = cursor.fetchone()[0]
        print(exists)
        cursor.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def check_table_is_full(con, user_id, table):
    exists = False
    try:
        cursor = con.cursor()
        cursor.execute('SELECT EXISTS(SELECT * FROM ' + table + ' WHERE user_id = ' + user_id + ');')
        exists = cursor.fetchone()[0]
        print(exists)
        cursor.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def getUserID(con, table):
    exists = 0
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM ' + table + ' WHERE id = 1')
        exists = cursor.fetchone()
        print(exists)
        cursor.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def getNote(con, week_id, user_id):
    exists = ''
    try:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM life WHERE week = ' + week_id + ' AND user_id = ' + user_id)
        exists = cursor.fetchone()[4]
        print(exists)
        cursor.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def changeNote(con, user_id, week_id, newNote):
    try:
        cursor = con.cursor()
        cursor.execute("UPDATE life SET note = '" + newNote + "' WHERE week = " + week_id + " AND user_id = " + user_id)
        con.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(e)

def populate_table_all(con, table_name, user_id, date_of_birth=1571):

    max_age = 4681
    data = []
    print(date_of_birth)

    a = (user_id,0,0)

    for i in range(1, date_of_birth):
        a = (user_id,i,0)
        data.append(a)

    a = (user_id,date_of_birth,1)
    data.append(a)

    for i in range(date_of_birth+1, max_age):
        a = (user_id,i,2)
        data.append(a)

    cursor = con.cursor()
    '''
    cursor.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (id SERIAL PRIMARY KEY,'
                                                        'user_id SMALLINT NOT NULL'
                                                        'week SMALLINT NOT NULL,'
                                                        'week_type SMALLINT NOT NULL,'
                                                        'note TEXT,'
                                                        'last_update DATE);'
                                                        )
    '''
    insert_query = "INSERT INTO " + table_name + " (user_id, week, week_type) VALUES %s"
    print('succes')
    psycopg2.extras.execute_values(cursor, insert_query, data)

    print('second milestone')
    con.commit()

    cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
