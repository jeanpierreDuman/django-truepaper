from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import csv
import sqlite3
from sqlite3 import Error


def determine(sentence):
    newsTrainer = Trainer(tokenizer)
    newsSet = []

    with open('data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            newsSet.append({'fact': row['Fact'], 'decision': row['Decision']})

    for news in newsSet:
        newsTrainer.train(news['fact'], news['decision'])

    newsClassifier = Classifier(newsTrainer.data, tokenizer)
    classification = newsClassifier.classify(sentence)
    # False
    false = classification[0][1]
    false = str(false).split('.')[0]
    # True
    true = classification[1][1]
    true = str(true).split('.')[0]
    data = [true, false]
    return data


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def add_point_to_machine():

    conn = create_connection('../db.sqlite3')

    cur = conn.cursor()
    cur.execute("SELECT * FROM app_fact")
    rows = cur.fetchall()

    for row in rows:
        data = determine(row[1])
        cursor = conn.cursor()
        cursor.execute("Update app_article SET machineGoodPoint=" + str(data[0]) + ", machineBadPoint=" + str(data[1]) + " WHERE id=" + str(row[5]))
        conn.commit()

    return len(rows)

add_point_to_machine()

print("Add machine point, Done !")