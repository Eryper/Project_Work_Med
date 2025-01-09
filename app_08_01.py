import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import plotly.graph_objects as go
import plotly.io as pio
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

def get_limiti_combinazione(pressa, tag_stampo, part_number, ordine):
    conn = sqlite3.connect('DatabaseSql/MTD.db')
    cursor = conn.cursor()
    query = """
        SELECT Parametro, Limite_inf, Limite_sup
        FROM Limiti
        WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Ordine = ?
    """
    cursor.execute(query, (pressa, tag_stampo, part_number, ordine))
    limiti = cursor.fetchall()
    conn.close()
    return limiti

@app.route('/api/Tag_stampo', methods=['GET'])

def get_Tag_stampo_filtrati():
    # Recupera i parametri dalla richiesta GET
    pressa = request.args.get('filtro0')


    # Verifica che i parametri siano presenti
    if not (pressa):
        return jsonify([])  # Se mancano parametri, restituisci lista vuota

    # Query filtrata
    query = """
        SELECT DISTINCT TAG_Stampo
        FROM Ordini
        WHERE codice_pressa = ?
        
    """
    Tag_stampi = get_data_from_db(query, (pressa,))
    
    return jsonify([{"id": Tag_stampo[0], "nome": Tag_stampo[0]} for Tag_stampo in Tag_stampi])

@app.route('/api/part_number', methods=['GET'])

def get_part_number_filtrati():
    # Recupera i parametri dalla richiesta GET
    pressa = request.args.get('filtro4')
    tag_stampo = request.args.get('filtro5')


    # Verifica che i parametri siano presenti
    if not (pressa and tag_stampo ):
        return jsonify([])  # Se mancano parametri, restituisci lista vuota

    # Query filtrata
    query = """
        SELECT DISTINCT part_number
        FROM Ordini
        WHERE codice_pressa = ? AND TAG_Stampo = ? 
        
    """
    part_numbers = get_data_from_db(query, (pressa, tag_stampo))

    # Restituisci i dati in formato JSON
    return jsonify([{"id": part_number[0], "nome": part_number[0]} for part_number in part_numbers])
    
@app.route('/api/ordine', methods=['GET'])

def get_ordini_filtrati():
    # Recupera i parametri dalla richiesta GET
    pressa = request.args.get('filtro1')
    tag_stampo = request.args.get('filtro2')
    part_number = request.args.get('filtro3')

    # Verifica che i parametri siano presenti
    if not (pressa and tag_stampo and part_number):
        return jsonify([])  # Se mancano parametri, restituisci lista vuota

    # Query filtrata
    query = """
        SELECT DISTINCT ordine
        FROM Ordini
        WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ?
        ORDER BY ordine ASC
    """
    ordini = get_data_from_db(query, (pressa, tag_stampo, part_number))

    # Restituisci i dati in formato JSON
    return jsonify([{"id": ordine[0], "nome": ordine[0]} for ordine in ordini])


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

@app.route('/inserimento_limiti', methods=['POST', 'GET'])
def inserimento_limiti():
    pressa = request.form.get('codice_pressa')
    tag_stampo = request.form.get('TAG_stampo')
    part_number = request.form.get('part_number')
    ordine = request.form.get('ordine')
    
    if ordine == 'Tutti': 
            # Query filtrata
        query = """
            SELECT DISTINCT ordine
            FROM Ordini
            WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ?
            ORDER BY ordine ASC
        """
        ordini = get_data_from_db(query, (pressa, tag_stampo, part_number))
        for multi_ordine in ordini:
            ordine = multi_ordine[0]
            query_parametri = """
                SELECT DISTINCT Parametro, U_M
                FROM Ordini
                JOIN Parametri ON Ordini.Ordine = Parametri.ordine
                WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
            """
        parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine))

    # Recupera i limiti se esistono già per questa combinazione
        query_limiti = """
            SELECT Parametro, Limite_inf, Limite_sup
            FROM Limiti
            WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Ordine = ?
        """
        limiti_esistenti = get_data_from_db(query_limiti, (pressa, tag_stampo, part_number, ordine))

    # Precompilazione dei limiti esistenti
        limiti_dict = {limite[0]: {'inf': limite[1], 'sup': limite[2]} for limite in limiti_esistenti}
        return render_template('inserimento_limiti.html',                         
                                        pressa=pressa, 
                                        tag_stampo=tag_stampo, 
                                        part_number=part_number,  
                                        orders = ordine,
                                        parametri=parametri,
                                        limiti_dict=limiti_dict)
    else :
    # Recupera i parametri dalla join tra le tabelle ordini e parametri
        query_parametri = """
            SELECT DISTINCT Parametro, U_M
            FROM Ordini
            JOIN Parametri ON Ordini.Ordine = Parametri.ordine
            WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
        """
        parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine))

    # Recupera i limiti se esistono già per questa combinazione
        query_limiti = """
            SELECT Parametro, Limite_inf, Limite_sup
            FROM Limiti
            WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Ordine = ?
        """
        limiti_esistenti = get_data_from_db(query_limiti, (pressa, tag_stampo, part_number, ordine))

    # Precompilazione dei limiti esistenti
        limiti_dict = {limite[0]: {'inf': limite[1], 'sup': limite[2]} for limite in limiti_esistenti}

        return render_template('inserimento_limiti.html', 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine, 
                           
                           parametri=parametri,
                           limiti_dict=limiti_dict)  # Passa i limiti precompilati
   

@app.route('/submit_limiti', methods=['POST'])
def submit_limiti():
    
    conn = sqlite3.connect('DatabaseSql/MTD.db')
    cursor = conn.cursor()

    pressa = request.form['codice_pressa']
    tag_stampo = request.form['TAG_stampo']
    part_number = request.form['part_number']
    ordine = request.form['ordine']
    orders = request.form['orders']
    # Stampa tutti i dati inviati
    print("Dati 2", request.form)
    
    # Verifica singoli valori
    if not (pressa and tag_stampo and part_number and  ordine or orders):
        print("Errore: campi obbligatori mancanti!")
        return "Errore: campi obbligatori mancanti!", 400

    parametri = request.form.getlist('Parametro')
    # Aggiungi una lista per i limiti
    limiti_inferiori = []
    limiti_superiori = []

    for parametro in parametri:
        limite_inf = request.form[f"Limite_inf{parametro}"]
        limite_sup = request.form[f"Limite_sup{parametro}"]
        print(f"Parametro: {parametro}, Limite_inf: {limite_inf}, Limite_sup: {limite_sup}")

        # Aggiungi i limiti a delle liste per usarli nel reindirizzamento
        limiti_inferiori.append(limite_inf)
        limiti_superiori.append(limite_sup)

        # Controllo validità valori
        if limite_inf is None or limite_sup is None:
            print(f"Errore: Limiti mancanti per il parametro {parametro}")
            continue
        

        # Verifica se esiste già il record
        cursor.execute("""
            SELECT 1 FROM limiti 
            WHERE Ordine = ? AND Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Parametro = ?
        """, (ordine, pressa, tag_stampo, part_number, parametro))

        existing_record = cursor.fetchone()

        if existing_record:

         # Se esiste, esegui un UPDATE
            cursor.execute(f"""
                UPDATE Limiti
                SET Limite_inf = {limite_inf}, Limite_sup = {limite_sup}
                WHERE Ordine = ? AND Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Parametro = ?
            """, (ordine, pressa, tag_stampo, part_number, parametro))
        else:
            # Se non esiste, esegui un INSERT
            cursor.execute("""
                INSERT INTO Limiti (Ordine, Pressa, Tag_stampo, Part_number, Parametro, Limite_inf, Limite_sup)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ordine, pressa, tag_stampo, part_number, parametro, limite_inf, limite_sup))

    print("Limiti salvati correttamente.")
    conn.commit()
    conn.close()

    # Reindirizza alla pagina dei grafici, passando anche i limiti inferiore e superiore
    return redirect(url_for('grafici', 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine,
                           limite_inf=limiti_inferiori,
                           limite_sup=limiti_superiori))



@app.route('/grafici', methods=['GET'])
def grafici():
    pressa = request.args.get('pressa')
    tag_stampo = request.args.get('tag_stampo')
    part_number = request.args.get('part_number')
    ordine = request.args.get('ordine')
    print("dati 3",pressa, tag_stampo, part_number, ordine)
    print(request.args)
    # Recupera i limiti dalla richiesta
    limite_inf = request.args.getlist('limite_inf', type=float)  # Limiti inferiori
    limite_sup = request.args.getlist('limite_sup', type=float)  # Limiti superiori

    # Query per ottenere parametri, valori e timestamp
    query = """
        SELECT Parametro, Valore, Ora 
        FROM Parametri 
        WHERE Ordine = ? 
        ORDER BY Parametro ASC
    """
    results = get_data_from_db(query, (ordine,))

    # Prepara i dati per il grafico
    parametri = {}
    for row in results:
        parametro,valore, ora = row
        if parametro not in parametri:
            parametri[parametro] = {'x': [], 'y': [], 'limite_inf': None, 'limite_sup': None}
        parametri[parametro]['x'].append(ora)  # Ora come x
        
        parametri[parametro]['y'].append(valore)  # Valore come y

    # Associa i limiti inferiore e superiore per ogni parametro
    # Supponiamo che i limiti siano passati nell'ordine in cui sono stati inseriti
    print("risultati",results)
    for i, parametro in enumerate(parametri):
        # Associa il limite inferiore e superiore per ogni parametro
        if i < len(limite_inf):
            parametri[parametro]['limite_inf'] = limite_inf[i]
        if i < len(limite_sup):
            parametri[parametro]['limite_sup'] = limite_sup[i]
        
    # Creazione dei grafici per ogni parametro
    graphs = []
    for parametro, data in parametri.items():
        fig = go.Figure()

        # Aggiungi il grafico dei dati come punti
        fig.add_trace(go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='markers',
            name=parametro,
            marker=dict(
                color='blue',
                size=10,
                line=dict(width=2, color='black')
            )
        ))

        # Aggiungi le linee per i limiti inferiore e superiore, se esistono
        if data['limite_inf'] is not None:
            fig.add_shape(
                type="line", 
                x0=min(data['x']), 
                x1=max(data['x']), 
                y0=data['limite_inf'],  # Usa il limite per il parametro specifico
                y1=data['limite_inf'],
                line=dict(color="red", dash="dash")
            )
        if data['limite_sup'] is not None:
            fig.add_shape(
                type="line", 
                x0=min(data['x']), 
                x1=max(data['x']), 
                y0=data['limite_sup'],  # Usa il limite per il parametro specifico
                y1=data['limite_sup'],
                line=dict(color="green", dash="dash")
            )

        # Aggiorna layout con titoli e assi
        fig.update_layout(
            title=f'Grafico per {parametro}',
            xaxis_title='Tempo',
            yaxis_title='Valore'
        )

        # Converte la figura in HTML e la aggiungi alla lista dei grafici
        graph_html = pio.to_html(fig, full_html=False)
        graphs.append(graph_html)

    # Passa i grafici come variabili al template
    return render_template('grafici.html', 
                           graphs=graphs, 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine)




    
if __name__ == '__main__':
    app.run(debug=True)








