from flask import Flask
from flask import send_file
from flask import render_template
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

links = {"Download": "/download",
         "Pairplot": "/pairplot",
         "Fair vs Pclass": "fair_vs_pclass",
         "PClass vs Sex": "pclass_vs_sex"}


def render_index(image=None):
    return render_template("index.html", links=links, image=image, code=time.time())


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", links=links, image=None)


@app.route('/download', methods=['GET'])
def download_data():
    return send_file("data/titanic_train.csv", as_attachment=True)


@app.route('/pairplot', methods=['GET'])
def pairplot():
    data = pd.read_csv("data/titanic_train.csv")
    sns_plot = sns.pairplot(data, hue="Survived")
    sns_plot.savefig("static/tmp/pairplot.png")
    return render_index(("pairplot.png", "Pairplot"))


@app.route('/fair_vs_pclass', methods=['GET'])
def fair_vs_pclass():
    fig, ax = plt.subplots()
    data = pd.read_csv("data/titanic_train.csv")
    filtered_data = data.query('Fare < 200')
    sns.boxplot(x='Pclass', y='Fare', data=filtered_data, ax=ax)
    plt.savefig('static/tmp/fair_vs_pclass.png')

    return render_index(("fair_vs_pclass.png", "Fair vs PClass plot"))


@app.route('/pclass_vs_sex', methods=['GET'])
def pclass_vs_sex():
    fig, ax = plt.subplots()
    data = pd.read_csv("data/titanic_train.csv")
    result = {}
    for (cl, sex), sub_df in data.groupby(['Pclass', 'Sex']):
        result[f"{cl} {sex}"] = sub_df['Age'].mean()

    plt.bar(result.keys(), result.values())
    plt.savefig('static/tmp/pclass_vs_sex.png')
    return render_index(("pclass_vs_sex.png", "PClass vs Sex graph"))


# app.run()
