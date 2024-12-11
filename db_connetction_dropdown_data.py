
# import sqlite3
# from flask import Flask, render_template

def get_data_from_db(query):
    # Connessione al database
    conn = sqlite3.connect('nome_del_tuo_database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()  # Recupera tutti i dati dalla query
    conn.close()
    return results

# @app.route('/')
def index():
    # Esegui le query per i dati dei dropdown
    query_pressa = "SELECT DISTINCT codice_pressa FROM ordini ORDER BY codice_pressa DESC"
    query_tag_stampo = "SELECT DISTINCT TAG_Stampo FROM ordini ORDER BY codice_pressa DESC"
    query_part_number = "SELECT DISTINCT part_number FROM ordini ORDER BY codice_pressa DESC"
    query_ordine = "SELECT DISTINCT ordine FROM ordini ORDER BY codice_pressa DESC"
    
    import_pressa = get_data_from_db(query_pressa)
    import_tag_stampo = get_data_from_db(query_tag_stampo)
    import_part_number = get_data_from_db(query_part_number)
    import_ordine = get_data_from_db(query_ordine)

    # Passa i dati al template
    return render_template('index.html', data_pressa=import_pressa, data_tag_stampo=import_tag_stampo, data_part_number=import_part_number, data_ordine=import_ordine)
