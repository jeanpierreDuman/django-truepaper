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


def reverse_old_point():

    conn = create_connection('../db.sqlite3')

    cur = conn.cursor()
    cur.execute("SELECT * FROM app_article")
    rows = cur.fetchall()

    for row in rows:
        cursor = conn.cursor()
        goodPoint = int(row[13])
        badPoint = int(row[14])
        oldGoodPoint = row[20]
        oldBadPoint = row[19]
        newGoodPoint = goodPoint - oldGoodPoint
        newBadPoint = badPoint - oldBadPoint

        if newGoodPoint < 0:
            newGoodPoint = 0

        if newBadPoint < 0:
            newBadPoint = 0

        cursor.execute("Update app_article SET goodPoint=" + str(newGoodPoint) + ", badPoint=" + str(newBadPoint) + ",machineGoodPoint=0, machineBadPoint=0,oldMachineGoodPoint=0, oldMachineBadPoint=0 WHERE id=" + str(row[0]))
        conn.commit()

    return len(rows)


reverse_old_point()

print("Reverse Done !")
