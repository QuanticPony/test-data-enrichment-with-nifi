import os, shutil
import sqlite3, json
# https://www.sqlitetutorial.net/sqlite-python/creating-tables/

TABLE_CREATE  = """CREATE TABLE IF NOT EXISTS users (
    ID      INT     NOT NULL,
    name    TEXT    NOT NULL,
    age     INT     NOT NULL,
    PRIMARY KEY (ID)    
    );"""


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        return c.execute(create_table_sql)
    except Exception as e:
        print(e)


def poblate_table(conn):
    names = ["Paco", "Roberto", "Alicia", "Pedro", "Andrés", "Gimena", "Pipo"]
    ages = [20,21,22,23,24,25,26]
    items_length = len(names)

    for i, (n, a) in enumerate(zip(names, ages)):
        try:
            c = conn.cursor()
        
            sentence = \
                f"INSERT INTO users VALUES (?,?,?);"

            c.execute(sentence, (i,n,a))

        except Exception as e:
            pass
        
def print_table(conn):
    try:
        c = conn.cursor()
        res =  c.execute("SELECT * FROM users;").fetchall()
        print(res)
        return res

    except Exception as e:
        print(e)

def poblate_in_subjects(path):
    for i in range(10):
        with open(f"{path}/{i}.json", 'w') as i_file:
            content = {'random_text': chr(65+i), 'ID': i}

            json.dump(content, i_file)

def removePreviousTests(MAIN_PATH):
    # Crear objetos "in" de prueba para enriquecer
    IN_PATH = MAIN_PATH + "/in"
    remove_from_path(IN_PATH)    
    poblate_in_subjects(IN_PATH)

    # Eliminar objetos en "out"
    OUT_PATH = MAIN_PATH + "/out"
    remove_from_path(OUT_PATH)  


def remove_from_path(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def main(path):
    MAIN_PATH = f"{'/'.join(__file__.split('/')[:-1])}"

    # Crear tabla y añadir objetos de prueba
    DB_FILE = MAIN_PATH + "/external_db.db"

    conn = create_connection(DB_FILE)
    if conn:
        create_table(conn, TABLE_CREATE)
        poblate_table(conn)
        conn.commit()
    print_table(conn)

    removePreviousTests(MAIN_PATH)    

if __name__=='__main__':
    main()