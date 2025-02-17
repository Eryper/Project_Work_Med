
# Importazione delle librerie necessarie
import pandas as pd  # pandas per la gestione dei dati in formato tabellare (dataframe)
import sqlite3  # sqlite3 per interagire con il database SQLite

# Definizione della dimensione del "chunk" per suddividere i dati in blocchi durante l'inserimento
chunk_size = 1000  # numero di righe per ogni blocco (chunk) da leggere e inserire

# Lettura dei file CSV in tre dataframe
file1 = pd.read_csv("Datasets/Ordini.csv", low_memory=None, delimiter=";", on_bad_lines='skip')  # Ordini.csv
file2 = pd.read_csv("Datasets/PC_puliti.csv", low_memory=None, delimiter=",", on_bad_lines='skip')  # PC_puliti.csv
file3 = pd.read_csv("Datasets/BOM_per_Ordine.csv", low_memory=None, delimiter=";", on_bad_lines='skip')  # BOM_per_Ordine.csv

# Estrazione dei nomi delle colonne dai file CSV letti
MyName = file1.columns  
MyName1 = file2.columns
MyName2 = file3.columns

# Connessione al database SQLite e creazione del cursore
conn = sqlite3.connect("DatabaseSql/MTD.db")  # Connessione al database SQLite (se il database non esiste, viene creato)
cursor = conn.cursor()  # Creazione del cursore per eseguire le operazioni SQL

# Creazione della tabella "Ordini" nel database, se non esiste già
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Ordini (
        Id_Ordine TEXT PRIMARY KEY,  # Definizione di un campo chiave primaria
        {MyName[0]} INTEGER,  # Altri campi derivanti dal CSV Ordini
        {MyName[1]} TEXT,
        {MyName[2]} TEXT,
        {MyName[3]} TEXT,
        {MyName[4]} TEXT,
        {MyName[5]} TEXT,
        {MyName[6]} TEXT       
        );
    """
)

# Creazione della tabella "Parametri" nel database, se non esiste già
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Parametri (
        Id_Parametro TEXT PRIMARY KEY,  # Definizione di un campo chiave primaria
        {MyName1[1]} INTEGER REFERENCES Ordini ({MyName[0]}),  # Collegamento alla tabella "Ordini" tramite chiave esterna
        {MyName1[2]} TEXT ,
        {MyName1[6]} TEXT ,
        {MyName1[7]} INTEGER,
        U_M CHAR(64)
        );
    """
)

# Creazione della tabella "BOM" nel database, se non esiste già
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS BOM(
            Id_Bom CHAR(64),
            {MyName2[0]} REFERENCES Ordini({MyName[0]}),  # Collegamento alla tabella "Ordini" tramite chiave esterna
            {MyName2[3]} CHAR(64),
            {MyName2[4]} CHAR(64)
        );
    """
)

# Creazione della tabella "Limiti" nel database, se non esiste già
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Limiti (
        id_limiti INTEGER PRIMARY KEY,  # Definizione di un campo chiave primaria
        Pressa TEXT,
        Tag_stampo TEXT,
        Part_number TEXT,
        Parametro TEXT, 
        Limite_inf INTEGER,
        Limite_sup INTEGER         
        );
    """
) 

# Ciclo per inserire i dati nella tabella "Ordini" dalla lettura del file CSV
try:
    for chunk1 in pd.read_csv("Datasets/Ordini.csv", chunksize=chunk_size, low_memory=None, delimiter=";", on_bad_lines='skip'):
        for index, row in chunk1.iterrows():
            try:
                # Inserimento dei dati nel database, ignorando le righe duplicate (usando INSERT OR IGNORE)
                cursor.execute(f"""
                    INSERT OR IGNORE INTO Ordini (Id_Ordine, {MyName[0]}, {MyName[1]},{MyName[2]},{MyName[3]},{MyName[4]},{MyName[5]},{MyName[6]})
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('OR'+str(index + 1), row[f"{MyName[0]}"], row[f"{MyName[1]}"], row[f"{MyName[2]}"], 
                      row[f"{MyName[3]}"], row[f"{MyName[4]}"], row[f"{MyName[5]}"], row[f"{MyName[6]}"]))
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()  # Esegui il commit delle modifiche al database dopo ogni chunk di righe
    
    # Ciclo per inserire i dati nella tabella "Parametri"
    for chunk2 in pd.read_csv("Datasets/PC_puliti.csv", chunksize=chunk_size, low_memory=None, delimiter=",", on_bad_lines='skip'):
        for index, row in chunk2.iterrows():
            try:
                # Inserimento dei dati nella tabella Parametri
                cursor.execute(f"""
                    INSERT OR IGNORE INTO Parametri (Id_Parametro, {MyName1[1]}, {MyName1[2]}, {MyName1[6]},{MyName1[7]},U_M)
                    VALUES (?, ?, ?, ?,?,?)
                """, ('PAR'+str(index + 1), row[f"{MyName1[1]}"], row[f"{MyName1[2]}"], row[f"{MyName1[6]}"], 
                      row[f"{MyName1[7]}"], row[f"{MyName1[9]}"]))
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()  # Esegui il commit dopo ogni blocco di righe

    # Ciclo per inserire i dati nella tabella "BOM"
    for chunk3 in pd.read_csv("Datasets/BOM_per_Ordine.csv", chunksize=chunk_size, low_memory=None, delimiter=";", on_bad_lines='skip'):
        for index, row in chunk3.iterrows():
            try:
                # Inserimento dei dati nella tabella BOM
                cursor.execute(f"""
                    INSERT OR IGNORE INTO BOM (Id_Bom, {MyName2[0]},{MyName2[3]},{MyName2[4]})
                    VALUES (?, ?, ?, ?)
                """, ('BOM'+str(index + 1), row[f"{MyName2[0]}"], row[f"{MyName2[3]}"], row[f"{MyName2[4]}"]))
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()  # Esegui il commit dopo ogni blocco di righe
    
except Exception as e:
    # Gestione degli errori durante l'importazione dei dati
    print(f"Errore durante l'importazione: {e}")

# Chiusura della connessione al database
conn.close()  # Chiude la connessione al database dopo l'inserimento
 
