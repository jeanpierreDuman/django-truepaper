import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_fact(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_fact")

    rows = cur.fetchall()

    data = []

    for row in rows:
        id_article = row[5]
        text = row[1]
        goodPoint = row[2]
        badPoint = row[3]
        decision = None

        if goodPoint > badPoint:
            decision = "True"
        elif goodPoint < badPoint:
            decision = "False"
        else:
            decision = "False"

        array = [str(id_article), text, decision]
        data.append(array)
    return data


def write_in_csv(datas):
    entetes = [
        u'Id',
        u'Fact',
        u'Decision',
    ]

    f = open('data.csv', 'w')
    ligneEntete = ",".join(entetes) + "\n"
    f.write(ligneEntete)
    for valeur in datas:
        ligne = ",".join(valeur).encode('utf-8').strip() + "\n"
        f.write(ligne)
    f.close()

con = create_connection('../db.sqlite3')

datas = select_fact(con)

write_in_csv(datas)

print("csv create, Done !")