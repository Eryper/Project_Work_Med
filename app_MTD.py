import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
import plotly.graph_objects as go
import plotly.io as pio
# libreria per convertire ordine in una lista
import ast

app = Flask(__name__)


# Funzione per ottenere i dati dal database
def get_data_from_db(query, params=None):
    """
    Esegue una query sul database SQLite e restituisce i risultati.
    
    :param query: La query SQL da eseguire
    :param params: Parametri per la query (opzionale)
    :return: Una lista di tuple contenente i risultati della query
    """
    conn = sqlite3.connect('DatabaseSql/MTD.db')  # Connessione al database
    cursor = conn.cursor()

    # Se i parametri sono forniti, passali alla query, altrimenti esegui senza parametri
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    results = cursor.fetchall()  # Ottieni tutti i risultati
    conn.close()  # Chiudi la connessione
    return results  # Restituisci i risultati


# Funzione per ottenere i limiti di combinazione da database
def get_limiti_combinazione(pressa, tag_stampo, part_number, ordine):
    """
    Ottiene i limiti associati a una combinazione di pressa, taglio stampo, 
    numero parte e ordine.
    
    :param pressa: Il nome della pressa
    :param tag_stampo: Il tag dello stampo
    :param part_number: Il numero di parte
    :param ordine: L'ordine
    :return: Una lista di tuple contenente i limiti per la combinazione
    """
    conn = sqlite3.connect('DatabaseSql/MTD.db')  # Connessione al database
    cursor = conn.cursor()
    
    # Query per selezionare i limiti dalla tabella 'Limiti'
    query = """
        SELECT Parametro, Limite_inf, Limite_sup
        FROM Limiti
        WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Ordine = ?
    """
    cursor.execute(query, (pressa, tag_stampo, part_number, ordine))  # Esegui la query con i parametri
    limiti = cursor.fetchall()  # Ottieni i risultati
    conn.close()  # Chiudi la connessione
    return limiti  # Restituisci i limiti

       

@app.route('/api/ordine', methods=['GET'])
def get_ordini_filtrati():
    # Recupera i parametri dalla richiesta GET
    pressa = request.args.get('filtro1')  
    tag_stampo = request.args.get('filtro2')  
    part_number = request.args.get('filtro3')  

    # Verifica che tutti i parametri siano presenti
    if not (pressa and tag_stampo and part_number):
        return jsonify([])  # Se mancano parametri, restituisci lista vuota

    # Costruisce la query per ottenere gli ordini filtrati
    query = """
        SELECT DISTINCT Ordini.ordine
        FROM Ordini
        INNER JOIN Parametri ON Ordini.ordine = Parametri.ordine
        WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ?
        ORDER BY Ordini.ordine ASC
    """
    # Esegui la query per ottenere gli ordini filtrati
    ordini = get_data_from_db(query, (pressa, tag_stampo, part_number))

    # Restituisci la lista di ordini in formato JSON
    return jsonify([{"id": ordine[0], "nome": ordine[0]} for ordine in ordini])



@app.route('/api/Tag_stampo', methods=['GET'])
def get_tag_stampo():
    # Ottieni i parametri filtro
    pressa = request.args.get('filtro1')
    part_number = request.args.get('filtro3')
    
    # Costruisce la query per ottenere i tag stampo
    query = "SELECT DISTINCT TAG_Stampo FROM Ordini WHERE 1=1"
    params = []  # Lista dei parametri per la query
    if pressa:
        query += " AND codice_pressa = ?"
        params.append(pressa)  # Aggiungi pressa se presente nel filtro
    if part_number:
        query += " AND part_number = ?"
        params.append(part_number)  # Aggiungi part_number se presente nel filtro
    
    # Esegui la query per ottenere i tag_stampo
    results = get_data_from_db(query, params)

    # Restituisci i risultati in formato JSON
    return jsonify([{"id": row[0], "nome": row[0]} for row in results])



@app.route('/api/part_number', methods=['GET'])
def get_part_number():
    # Ottieni i parametri filtro
    pressa = request.args.get('filtro1')
    tag_stampo = request.args.get('filtro2')

    # Costruisce la query per ottenere i part_number
    query = "SELECT DISTINCT part_number FROM Ordini WHERE 1=1"
    params = []  # Lista dei parametri per la query
    if pressa:
        query += " AND codice_pressa = ?"
        params.append(pressa)  # Aggiungi pressa se presente nel filtro
    if tag_stampo:
        query += " AND TAG_Stampo = ?"
        params.append(tag_stampo)  # Aggiungi tag_stampo se presente nel filtro

    # Esegui la query per ottenere i part_number
    results = get_data_from_db(query, params)

    # Restituisci i risultati in formato JSON
    return jsonify([{"id": row[0], "nome": row[0]} for row in results])



@app.route('/api/pressa', methods=['GET'])
def get_pressa():
    # Ottieni i parametri filtro
    tag_stampo = request.args.get('filtro2')
    part_number = request.args.get('filtro3')

    # Costruisce la query per ottenere le presse
    query = "SELECT DISTINCT codice_pressa FROM Ordini WHERE 1=1"
    params = []  # Lista dei parametri per la query
    if tag_stampo:
        query += " AND TAG_Stampo = ?"
        params.append(tag_stampo)  # Aggiungi tag_stampo se presente nel filtro
    if part_number:
        query += " AND part_number = ?"
        params.append(part_number)  # Aggiungi part_number se presente nel filtro
    
    # Esegui la query per ottenere le presse
    results = get_data_from_db(query, params)

    # Restituisci i risultati in formato JSON
    return jsonify([{"id": row[0], "nome": row[0]} for row in results])



@app.route('/', methods=['GET'])
def index():
    # Queries per recuperare i codici pressa, i tag stampo e i part number, ordinati in ordine decrescente
    query_pressa = "SELECT DISTINCT codice_pressa FROM Ordini ORDER BY codice_pressa DESC"
    query_tag_stampo = "SELECT DISTINCT TAG_Stampo FROM Ordini ORDER BY TAG_Stampo DESC"
    query_part_number = "SELECT DISTINCT part_number FROM Ordini ORDER BY part_number DESC"

    # Recupera i dati dalle query eseguite
    data_pressa = get_data_from_db(query_pressa)
    data_tag_stampo = get_data_from_db(query_tag_stampo)
    data_part_number = get_data_from_db(query_part_number)

    # Renderizza il template 'nuovo_selezione_codici.html' passando i dati recuperati
    return render_template('nuovo_selezione_codici.html', 
                           data_pressa=data_pressa,
                           data_tag_stampo=data_tag_stampo,
                           data_part_number=data_part_number
                           )



@app.route('/inserimento_limiti', methods=['POST', 'GET'])
def inserimento_limiti():
    # Recupera i parametri inviati dal form (pressa, tag_stampo, part_number, ordine)
    pressa = request.form.get('codice_pressa')
    tag_stampo = request.form.get('TAG_stampo')
    part_number = request.form.get('part_number')
    ordine = request.form.get('ordine')
    
    if ordine == 'Tutti':  # Se l'ordine è 'Tutti', recupera tutti gli ordini
        # Query per ottenere tutti gli ordini in base ai parametri specificati
        query = """
            SELECT DISTINCT Ordini.ordine
            FROM Ordini
            INNER JOIN Parametri ON Ordini.ordine = Parametri.ordine
            WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ?
            ORDER BY Ordini.ordine ASC
        """
        ordini = get_data_from_db(query, (pressa, tag_stampo, part_number))
        
        # Liste per raccogliere i parametri e limiti di tutti gli ordini
        parametri_totali = []
        limiti_totali = []
        
        # Per ogni ordine trovato, recupera i parametri e limiti associati
        for multi_ordine in ordini:
            ordine_corrente = multi_ordine[0]
            
            # Query per i parametri relativi a ciascun ordine
            query_parametri = """
                SELECT DISTINCT Parametro, U_M
                FROM Ordini
                JOIN Parametri ON Ordini.Ordine = Parametri.ordine
                WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
                ORDER BY Parametro ASC
            """
            parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine_corrente))
            parametri_totali.extend(set(parametri))  # Aggiunge i parametri unici alla lista
            
            # Query per i limiti relativi a ciascun ordine
            query_limiti = """
                SELECT DISTINCT Parametro, Limite_inf, Limite_sup
                FROM Limiti
                WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ?
                ORDER BY Parametro ASC
            """
            limiti = get_data_from_db(query_limiti, (pressa, tag_stampo, part_number))
            limiti_totali.extend(set(limiti))  # Aggiunge i limiti unici alla lista
        
        # Ordina i parametri e i limiti per nome
        parametri_totali = sorted(set(parametri_totali), key=lambda x: x[0])
        limiti_totali = sorted(set(limiti_totali), key=lambda x: x[0])
        
        # Creazione di un dizionario con i limiti (limite inferiore e superiore per ciascun parametro)
        limiti_dict = {limite[0]: {'inf': limite[1], 'sup': limite[2]} for limite in limiti_totali}

        # Passa i dati al template 'inserimento_limiti.html'
        return render_template(
            'inserimento_limiti.html',
            pressa=pressa,
            tag_stampo=tag_stampo,
            part_number=part_number,
            ordine=[ordine[0] for ordine in ordini],  # Lista degli ordini
            parametri=parametri_totali,
            limiti_dict=limiti_dict
        )
    else:
        # Se l'ordine è un singolo valore (non 'Tutti')
        
        # Query per i parametri del singolo ordine
        query_parametri = """
            SELECT DISTINCT Parametro, U_M
            FROM Ordini
            INNER JOIN Parametri ON Ordini.Ordine = Parametri.ordine
            WHERE codice_pressa = ? AND TAG_Stampo = ? AND part_number = ? AND Ordini.ordine = ?
            ORDER BY Parametro ASC
        """
        parametri = get_data_from_db(query_parametri, (pressa, tag_stampo, part_number, ordine))

        # Query per i limiti del singolo ordine
        query_limiti = """
            SELECT Parametro, Limite_inf, Limite_sup
            FROM Limiti
            WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ?
            ORDER BY Parametro ASC
        """
        limiti_esistenti = get_data_from_db(query_limiti, (pressa, tag_stampo, part_number))

        # Creazione del dizionario con i limiti (limite inferiore e superiore per ciascun parametro)
        limiti_dict = {limite[0]: {'inf': limite[1], 'sup': limite[2]} for limite in limiti_esistenti}

        # Passa i dati al template 'inserimento_limiti.html'
        return render_template(
            'inserimento_limiti.html',
            pressa=pressa,
            tag_stampo=tag_stampo,
            part_number=part_number,
            ordine=ordine,
            parametri=parametri,
            limiti_dict=limiti_dict
        )

   

@app.route('/submit_limiti', methods=['POST'])
def submit_limiti():
    # Connessione al database
    conn = sqlite3.connect('DatabaseSql/MTD.db')
    cursor = conn.cursor()

    # Recupera i dati dal form inviato
    pressa = request.form['codice_pressa']
    tag_stampo = request.form['TAG_stampo']
    part_number = request.form['part_number']
    ordine = request.form['ordine']
    
    # Log dei dati ricevuti per il debug
    print("Dati 2", request.form)
    
    # Verifica che tutti i campi obbligatori siano presenti
    if not (pressa and tag_stampo and part_number and ordine):
        print("Errore: campi obbligatori mancanti!")
        return "Errore: campi obbligatori mancanti!", 400

    # Ottiene la lista di parametri selezionati
    parametri = request.form.getlist('Parametro')
    
    # Liste per raccogliere i limiti inferiori e superiori
    limiti_inferiori = []
    limiti_superiori = []

    # Ciclo su ogni parametro per ottenere i limiti
    for parametro in parametri:
        limite_inf = request.form[f"Limite_inf{parametro}"]
        limite_sup = request.form[f"Limite_sup{parametro}"]
        
        # Log dei limiti ricevuti per il debug
        print(f"Parametro: {parametro}, Limite_inf: {limite_inf}, Limite_sup: {limite_sup}")

        # Aggiungi i limiti alle liste
        limiti_inferiori.append(limite_inf)
        limiti_superiori.append(limite_sup)

        # Verifica che i limiti siano validi
        if limite_inf is None or limite_sup is None:
            print(f"Errore: Limiti mancanti per il parametro {parametro}")
            continue
        
        # Verifica se esiste già un record per questo parametro
        cursor.execute("""
            SELECT 1 FROM limiti 
            WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Parametro = ?
        """, (pressa, tag_stampo, part_number, parametro))

        # Se il record esiste, esegui un UPDATE, altrimenti un INSERT
        existing_record = cursor.fetchone()

        if existing_record:
            # Aggiorna il limite esistente
            cursor.execute(f"""
                UPDATE Limiti
                SET Limite_inf = {limite_inf}, Limite_sup = {limite_sup}
                WHERE Pressa = ? AND Tag_stampo = ? AND Part_number = ? AND Parametro = ?
            """, (pressa, tag_stampo, part_number, parametro))
        else:
            # Inserisce un nuovo record con i limiti
            cursor.execute("""
                INSERT INTO Limiti (Pressa, Tag_stampo, Part_number, Parametro, Limite_inf, Limite_sup)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (pressa, tag_stampo, part_number, parametro, limite_inf, limite_sup))

    # Commit delle modifiche al database
    print("Limiti salvati correttamente.")
    conn.commit()
    conn.close()

    # Reindirizza alla pagina dei grafici con i dati relativi ai limiti
    return redirect(url_for('grafici', 
                           pressa=pressa, 
                           tag_stampo=tag_stampo, 
                           part_number=part_number, 
                           ordine=ordine,
                           limite_inf=limiti_inferiori,
                           limite_sup=limiti_superiori))



@app.route('/grafici', methods=['GET'])
def grafici():
    # Recupera i parametri dalla richiesta URL
    pressa = request.args.get('pressa')
    tag_stampo = request.args.get('tag_stampo')
    part_number = request.args.get('part_number')
    ordine = request.args.get('ordine')

    # Stampa i dati ricevuti per il debug
    print("dati 3", pressa, tag_stampo, part_number, ordine)
    print(request.args)

    # Recupera i limiti inferiori e superiori dalla richiesta URL
    limite_inf = request.args.getlist('limite_inf', type=float)  # Limiti inferiori
    limite_sup = request.args.getlist('limite_sup', type=float)  # Limiti superiori

    # Converte il parametro ordine in una lista, se non lo è già
    value = ast.literal_eval(ordine)
    new_ordine = []
    if not isinstance(value, list):
        new_ordine.append(value)
    else:
        new_ordine = value
    placeholders = ', '.join(['?'] * len(new_ordine))

    # Crea la query SQL per recuperare i dati dai parametri
    query = f"""
            SELECT P.Parametro, P.Valore, P.Ora, P.Ordine, P.U_M, O.lotto
            FROM Ordini as O
            INNER JOIN Parametri as P ON O.ordine = P.ordine
            WHERE P.ordine IN ({placeholders}) 
            ORDER BY P.Parametro ASC
        """
    results = get_data_from_db(query, tuple(new_ordine))

    # Prepara un dizionario per memorizzare i dati dei parametri
    parametri = {}
    for row in results:
        parametro, valore, ora, ordine_val, units_val, lotto_val = row
        if parametro not in parametri:
            parametri[parametro] = {'x': [], 'y': [], 'limite_inf': None, 'limite_sup': None, 'ordini': [], 'units': [], "lotti": []}
        parametri[parametro]['x'].append(ora)  # Ora come x
        parametri[parametro]['y'].append(valore)  # Valore come y
        parametri[parametro]['ordini'].append(ordine_val)  # Aggiungi il numero dell'ordine
        parametri[parametro]['units'].append(units_val)  # Aggiungi l'unità di misura
        parametri[parametro]['lotti'].append(lotto_val)

    # Associa i limiti inferiori e superiori per ogni parametro
    for i, parametro in enumerate(parametri):
        if i < len(limite_inf):
                parametri[parametro]['limite_inf'] = limite_inf[i]
        if i < len(limite_sup):
            parametri[parametro]['limite_sup'] = limite_sup[i]

    # Crea i grafici per ogni parametro
    graphs = []
    for parametro, data in parametri.items():
        fig = go.Figure()

        # Seleziona i punti "normali" che sono dentro i limiti
        normal_x = [data['x'][i] for i in range(len(data['x'])) if data['y'][i] >= data['limite_inf'] and data['y'][i] <= data['limite_sup']]
        normal_y = [data['y'][i] for i in range(len(data['y'])) if data['y'][i] >= data['limite_inf'] and data['y'][i] <= data['limite_sup']]
        normal_ordini = [data['ordini'][i] for i in range(len(data['ordini'])) if data['y'][i] >= data['limite_inf'] and data['y'][i] <= data['limite_sup']]
        normal_units = [data['units'][i] for i in range(len(data['units'])) if data['y'][i] >= data['limite_inf'] and data['y'][i] <= data['limite_sup']]
        normal_lotti = [data['lotti'][i] for i in range(len(data['lotti'])) if data['y'][i] >= data['limite_inf'] and data['y'][i] <= data['limite_sup']]

        # Seleziona i punti "outliers" che sono fuori dai limiti
        outlier_x = [data['x'][i] for i in range(len(data['x'])) if data['y'][i] < data['limite_inf'] or data['y'][i] > data['limite_sup']]
        outlier_y = [data['y'][i] for i in range(len(data['y'])) if data['y'][i] < data['limite_inf'] or data['y'][i] > data['limite_sup']]
        outlier_ordini = [data['ordini'][i] for i in range(len(data['ordini'])) if data['y'][i] < data['limite_inf'] or data['y'][i] > data['limite_sup']]
        outlier_units = [data['units'][i] for i in range(len(data['units'])) if data['y'][i] < data['limite_inf'] or data['y'][i] > data['limite_sup']]
        outlier_lotti = [data['lotti'][i] for i in range(len(data['lotti'])) if data['y'][i] < data['limite_inf'] or data['y'][i] > data['limite_sup']]

        # Aggiungi i punti normali (in blu)
        fig.add_trace(go.Scatter(
            x=normal_x,
            y=normal_y,
            mode='markers',
            marker=dict(
                color='blue',
                size=10,
                line=dict(width=2, color='black')
            ),
            hovertemplate=(  # Definisce la finestra pop-up al passaggio del mouse
                'Timestamp: %{x|%d %b %Y, %H:%M:%S}<br>' +
                'Valore: %{y} %{customdata[1]}<br>' +  # Mostra l'unità di misura
                'Ordine: %{customdata[0]}<br>' +  # Mostra l'ordine
                'Lotto: %{customdata[2]}<br>' +
                '<extra></extra>'  # Rimuove la barra informativa extra
            ),
            text=[parametro] * len(normal_x),
            customdata=list(zip(normal_ordini, normal_units, normal_lotti)),
            name='In Spec'  # Punti dentro i limiti
        ))

        # Aggiungi i punti outliers (in rosso, con simbolo X)
        fig.add_trace(go.Scatter(
            x=outlier_x,
            y=outlier_y,
            mode='markers',
            marker=dict(
                color='red',
                size=12,
                symbol='x',  # Utilizza la X per gli outliers
                line=dict(width=2, color='black')
            ),
            hovertemplate=(  # Definisce la finestra pop-up per gli outliers
                'Timestamp: %{x|%d %b %Y, %H:%M:%S}<br>' +
                'Valore: %{y} %{customdata[1]}<br>' +  # Mostra l'unità di misura
                'Ordine: %{customdata[0]}<br>' +  # Mostra l'ordine
                'Lotto: %{customdata[2]}<br>' +
                '<extra></extra>'  # Rimuove la barra informativa extra
            ),
            text=[parametro] * len(outlier_x),
            customdata=list(zip(outlier_ordini, outlier_units, outlier_lotti)),
            name='Out of Spec'  # Punti fuori dai limiti
        ))

        # Aggiungi le linee per i limiti inferiori e superiori
        if data['limite_inf'] is not None:
            fig.add_shape(
                type="line", 
                x0=min(data['x']), 
                x1=max(data['x']), 
                y0=data['limite_inf'],  # Limite inferiore
                y1=data['limite_inf'],
                line=dict(color="red", dash="dash")
            )
        if data['limite_sup'] is not None:
            fig.add_shape(
                type="line", 
                x0=min(data['x']), 
                x1=max(data['x']), 
                y0=data['limite_sup'],  # Limite superiore
                y1=data['limite_sup'],
                line=dict(color="red", dash="dash")
            )

        # Aggiorna il layout del grafico con titoli e assi
        fig.update_layout(
            title=f'{parametro}',
            title_font=dict(color='black',family='Arial', size=20, weight='bold'),
             xaxis=dict(
                title='Tempo',
                title_font=dict(color='black', weight='bold'),  # Colore dell'etichetta asse X
                tickfont=dict(color='black')  # Colore delle etichette asse X
            ),
            yaxis=dict(
                title='Valore',
                title_font=dict(color='black', weight='bold'),  # Colore dell'etichetta asse Y
                tickfont=dict(color='black')  # Colore delle etichette asse Y
            )
        )

        # Converte il grafico in HTML e lo aggiunge alla lista dei grafici
        graph_html = pio.to_html(fig, full_html=False)
        graphs.append(graph_html)

    # Passa i grafici come variabili al template HTML
    return render_template('grafici.html', 
                        graphs=graphs, 
                        pressa=pressa, 
                        tag_stampo=tag_stampo, 
                        part_number=part_number, 
                        ordine=ordine)


# Avvia l'app Flask
if __name__ == '__main__':
    app.run(debug=True)

    