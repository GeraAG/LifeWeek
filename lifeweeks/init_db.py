import psycopg2
import psycopg2.extras

database = 'lifeweeks'
conn = psycopg2.connect("dbname='" + database + "' user='postgres' host='localhost' password='dasKuli4'")

cursor = conn.cursor()
#cursor.execute('DROP TABLE IF EXISTS life;')
cursor.execute('CREATE TABLE IF NOT EXISTS life (id SERIAL PRIMARY KEY,'
                                                'user_id SMALLINT NOT NULL,'
                                                'week SMALLINT NOT NULL,'
                                                'week_type SMALLINT NOT NULL,'
                                                'note TEXT,'
                                                'last_update DATE);'
                                                )

cursor.execute('DROP TABLE IF EXISTS users;')
cursor.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,'
                                                'email VARCHAR (100) NOT NULL UNIQUE,'
                                                'name VARCHAR (100) NOT NULL,'
                                                'password VARCHAR(1000) NOT NULL,'
                                                'date_of_birth DATE NOT NULL);'
                                                )
#cursor.execute('INSERT INTO users (name, birthday) VALUES (%s, %s)', ('andrej', "1993-10-01"))

conn.commit()
cursor.close()
if conn:
    conn.close()
