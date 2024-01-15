from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

current_age = 1571
VALID_COLUMN = {'user_id', 'week', 'week_type', 'note', 'last_update', 'email', 'name', 'password', 'date_of_birth'}


@app.route("/")
def home():
    database = 'lifeweeks'
    conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")

    table_exists_users = table_exists(conn, database, 'users')
    user_id = '1'
    user = ()
    current_age = 1571
    if table_exists_users:
        user = get_user_ID(conn, 'users')
        user_id = str(user[0])
        #current_age = getAgeInWeeks(user[2])
        user_name = user[1]

    table_name = 'life'
    table_exists_life = table_exists(conn, database, table_name)

    table_is_full = False
    if table_exists_life:
        table_is_full = check_table_has_user_data(conn, 'user_id', user_id, table_name)

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

        note = get_note(conn, week_id, user_id)
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

        change_note(conn, user_id, week_id, newNote)

        if conn:
            conn.close()

        return 'Success'

@app.route("/login")
def login():
    return 'Login'

@app.route("/signup", methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        date_of_birth = request.form.get('date_of_birth')

        # check if user already exists (YES - redirect to signup)
        database = 'lifeweeks'
        conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")
        table_name = 'users'
        table_exists_users = table_exists(conn, database, table_name)

        email_exists = False
        if table_exists_users:
            email_exists = check_table_has_user_data(conn, 'email', email, table_name)
            if email_exists:
                return redirect(url_for('app.signup'))
        else:
            raise ValueError('Table does not exist')

        if not email_exists:
            new_user = {}
            new_user['email'] = email
            new_user['name'] = name
            new_user['password'] = password
            new_user['date_of_birth'] = date_of_birth

            if add_new_user(conn, new_user):
                return redirect(url_for('app.login'))
            else:
                #Change after testing
                raise ValueError('Error creating new user')
    else:
        return render_template('signup.html')

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

def check_table_has_user_data(con, column, value, table):
    exists = False
    if column not in VALID_COLUMN:
        raise ValueError("column: name of column must be one of %r." % VALID_COLUMN)

    try:
        cursor = con.cursor()
        cursor.execute('SELECT EXISTS(SELECT * FROM ' + table + ' WHERE ' + column + ' = ' + value + ');')

        # delete if sign up works
        # --START--
        i = 0
        match column:
            case 'user_id':
                i = 1
            case 'week':
                i = 2
            case 'week_type':
                i = 3
            case 'note':
                i = 4
            case 'last_update':
                i = 5
            case 'email':
                i = 1
            case 'name':
                i = 2
            case 'password':
                i = 3
            case 'date_of_birth':
                i = 4
        #--END--

        exists = cursor.fetchone()[0]
        print(exists)
        cursor.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def get_user_ID(con, table):
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

def get_note(con, week_id, user_id):
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

def change_note(con, user_id, week_id, newNote):
    try:
        cursor = con.cursor()
        cursor.execute("UPDATE life SET note = (%s) WHERE week = (%s) AND user_id = (%s)", (newNote, week_id, user_id))
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

def add_new_user(con, new_user):
    try:
        cursor = con,cursor()
        cursor.execute("INSERT INTO users (email, name, password, date_of_birth) VALUES ((%s), (%s), (%s), (%s));", (new_user['email'], new_user['name'], new_user['password'], new_user['date_of_birth']))
        con.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(e)

if __name__ == '__main__':
    app.run(debug=True)
