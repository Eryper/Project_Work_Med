import plotly.express as px
from flask import Flask, render_template, request
import time
import pandas as pd
import random as rd
import sqlite3

def get_data_from_db(query):
    # Connessione al database
    conn = sqlite3.connect('Datasets/MTD.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()  # Recupera tutti i dati dalla query
    
    return results

def index():
    # Esegui le query per i dati dei dropdown
    query_pressa = "SELECT DISTINCT codice_pressa FROM Ordini ORDER BY codice_pressa DESC"
    query_tag_stampo = "SELECT DISTINCT TAG_Stampo FROM ordini ORDER BY codice_pressa DESC"
    query_part_number = "SELECT DISTINCT part_number FROM ordini ORDER BY codice_pressa DESC"
    query_ordine = "SELECT DISTINCT ordine FROM ordini ORDER BY codice_pressa DESC"
    
    import_pressa = get_data_from_db(query_pressa)
    import_tag_stampo = get_data_from_db(query_tag_stampo)
    import_part_number = get_data_from_db(query_part_number)
    import_ordine = get_data_from_db(query_ordine)
    return render_template('selezione_codici.html', data_pressa=import_pressa, data_tag_stampo=import_tag_stampo, data_part_number=import_part_number, data_ordine=import_ordine)

app = Flask(__name__)
@app.route('/')
def graph():

    return  render_template("selezione_codici.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
