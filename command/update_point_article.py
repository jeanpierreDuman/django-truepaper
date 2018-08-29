from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import csv
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def update_point_article():

    conn = create_connection('../db.sqlite3')

    cur = conn.cursor()
    cur.execute("SELECT * FROM app_article")
    rows = cur.fetchall()

    for row in rows:
        cursor = conn.cursor()
        goodPoint = int(row[13])
        badPoint = int(row[14])
        oldGoodPoint = int(row[18])
        oldBadPoint = int(row[17])
        newGoodPoint = goodPoint + oldGoodPoint
        newBadPoint = badPoint + oldBadPoint
        cursor.execute("Update app_article SET oldMachineGoodPoint=" + str(oldGoodPoint) + ", oldMachineBadPoint=" + str(oldBadPoint) + ", goodPoint=" + str(newGoodPoint) + ", badPoint=" + str(newBadPoint) + " , machineGoodPoint=0, machineBadPoint=0 WHERE id=" + str(row[0]))
        conn.commit()


    return len(rows)


update_point_article()

print("Update machine point, Done !")