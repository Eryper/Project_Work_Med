import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_data_from_db(query, params=None):
    conn = sqlite3.connect('C:/Users/studente/Desktop/PW MEDTRONIC/Project_Work_Med/DatabaseSql/MTD.db')
    cursor = conn.cursor()

     # Se i parametri sono forniti, passali alla query, altrimenti esegui senza parametri
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/', methods=['GET'])
def index():
    query_pressa = "SELECT DISTINCT codice_pressa FROM Ordini ORDER BY codice_pressa DESC"
    query_tag_stampo = "SELECT DISTINCT TAG_Stampo FROM Ordini ORDER BY codice_pressa DESC"
    query_part_number = "SELECT DISTINCT part_number FROM Ordini ORDER BY codice_pressa DESC"
    query_ordine = "SELECT DISTINCT ordine FROM Ordini ORDER BY codice_pressa DESC"

    data_pressa = get_data_from_db(query_pressa)
    data_tag_stampo = get_data_from_db(query_tag_stampo)
    data_part_number = get_data_from_db(query_part_number)
    data_ordine = get_data_from_db(query_ordine)

    return render_template('selezione_codici_definitivo_2.html', 
                           data_pressa=data_pressa, 
                           data_tag_stampo=data_tag_stampo, 
                           data_part_number=data_part_number, 
                           data_ordine=data_ordine)

@app.route('/inserimento_limiti', methods=['POST'])
def inserimento_limiti():
    pressa = request.form['codice_pressa']
    tag_stampo = request.form['tag_stampo']
    part_number = request.form['part_number']
    ordine = request.form['ordine']

    # Recupera i parametri dalla join tra le tabelle ordini e parametri
    query_parametri = """
        SELECT DISTINCT parametro
        FROM Ordini
        JOIN Parametri ON ordini.ordine = parametri.ordine
        WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
    """
    parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine))

    return render_template('inserimento_limiti.html', 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine, 
                           parametri=parametri)

@app.route('/submit_limiti', methods=['POST'])
def submit_limiti():
    pressa = request.form['Pressa']
    tag_stampo = request.form['Tag_stampo']
    part_number = request.form['Part_number']
    ordine = request.form['Ordine']

    parametri = request.form.getlist('parametro')
    
    print(f"Pressa: {pressa}, Tag Stampo: {tag_stampo}, Part Number: {part_number}, Ordine: {ordine}")
    print(f"Parametri: {parametri}")


    for parametro in parametri:
        limite_inf = request.form[f"limite_inf_{parametro}"]
        limite_sup = request.form[f"limite_sup_{parametro}"]
        
        print(f"Parametro: {parametro}, Limite Inferiore: {limite_inf}, Limite Superiore: {limite_sup}")

        query = """
        INSERT INTO Limiti (Pressa, Tag_stampo, Part_number, Ordine, Parametro, Limite_inf, Limite_sup)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (pressa, tag_stampo, part_number, ordine, parametro, limite_inf, limite_sup)
        
        conn = sqlite3.connect('C:/Users/studente/Desktop/PW MEDTRONIC/Project_Work_Med/DatabaseSql/MTD.db')
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
