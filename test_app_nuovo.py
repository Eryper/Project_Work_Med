import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
app = Flask(__name__)

def get_data_from_db(query, params=None):
    conn = sqlite3.connect('DatabaseSql/MTD.db')
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

    return render_template('selezione_codici_definitivo.html', 
                           data_pressa=data_pressa, 
                           data_tag_stampo=data_tag_stampo, 
                           data_part_number=data_part_number, 
                           data_ordine=data_ordine)

@app.route('/inserimento_limiti', methods=['POST'])
def inserimento_limiti():
    
    pressa = request.form['codice_pressa']
    tag_stampo = request.form['TAG_stampo']
    part_number = request.form['part_number']
    ordine = request.form['ordine']
    print("Dati 1", request.form)
    # Recupera i parametri e le unita di misura dalla join tra le tabelle ordini e parametri
    query_parametri = """
        SELECT DISTINCT Parametro, U_M
        FROM Ordini
        JOIN Parametri ON Ordini.Ordine = Parametri.ordine
        WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
    """
    parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine))

    # query per ottenere i valori
    query_valori = """
        SELECT Valore
        FROM Ordini
        JOIN Parametri ON Ordini.Ordine = Parametri.ordine
        WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
    """
    valori = get_data_from_db(query_valori, (pressa, tag_stampo, part_number, ordine))
    print(f"Parametri ricevuti 1: {parametri}") # print per vedere nel debug

    # Recupera tutti i valori da inserire poi nella control chart 

    
    return render_template('inserimento_limiti.html', 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine, 
                           parametri=parametri,
                           valori= valori)

@app.route('/submit_limiti', methods=['POST'])
def submit_limiti():
    conn = sqlite3.connect('DatabaseSql/MTD.db')
    cursor = conn.cursor()



    pressa = request.form['codice_pressa']
    tag_stampo = request.form['TAG_stampo']
    part_number = request.form['part_number']
    ordine = request.form['ordine']

    # Stampa tutti i dati inviati
    print("Dati 2", request.form)
    # Verifica singoli valori
    if not (pressa and tag_stampo and part_number and ordine):
        print("Errore: campi obbligatori mancanti!")
        return "Errore: campi obbligatori mancanti!", 400

    parametri = request.form.getlist('Parametro')
    valori = request.form.getlist('Valore')
    print(f"Parametri ricevuti 2: {parametri}")
    for parametro in parametri:
        parametri = [p[0] for p in parametri]  # Estrai solo il primo elemento di ogni tupla
        limite_inf = request.form[f"Limite_inf{parametro}"]
        limite_sup = request.form[f"Limite_sup{parametro}"]
        print(f"Parametro: {parametro}, Limite_inf: {limite_inf}, Limite_sup: {limite_sup}")
        
        # Controllo validità valori
        if limite_inf is None or limite_sup is None:
            print(f"Errore: Limiti mancanti per il parametro {parametro}")
            continue

        query_limiti = """
        INSERT INTO Limiti (Ordine, Pressa, Tag_stampo, Part_number, Parametro, Limite_inf, Limite_sup)
        VALUES ( ?, ?, ?,?,?,?,?)
        """
        values = ( ordine, pressa ,tag_stampo,part_number , parametro, limite_inf, limite_sup)

        print(f"Query: {query_limiti}")
        print(f"Values: {values}")
        cursor.execute(query_limiti, values)
    print("I miei valori",valori)
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))
#@app.route("/make_graph")
# def genera_grafico():
#    valori = request.form['Valore']
#     fig = go.Figure()

    # Linea centrale

    # Limiti superiori e inferiori
    # fig.add_trace(go.Scatter(x=df['Sample'], y=[UCL] * len(df),
    #                    mode='lines', name='UCL', line=dict(color='red', dash='dot')))
    # fig.add_trace(go.Scatter(x=df['Sample'], y=[LCL] * len(df),
    #                    mode='lines', name='LCL', line=dict(color='red', dash='dot')))

    # Dati reali
    # fig.add_trace(go.Scatter(x=df['Sample'], y=df['Value'],
    #                    mode='markers+lines', name='Valori', marker=dict(color='green')))

    # Layout
    # fig.update_layout(title='Carta di Controllo',
    #              xaxis_title='Campioni',
    #             yaxis_title='Valore',
    #             template='plotly_white')
    # fig.show()



    
if __name__ == '__main__':
    app.run(debug=True)
