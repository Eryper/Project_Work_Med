#Questo scrpit permette la creazione di una tabella sql e l'inserimento dei dati del file csv nella tabella sql
# librerie necessarie
import pandas as pd 
import sqlite3 
import time

chunk_size =1000 # n di righe per dividere il database
# importazione del file csv con pandas e creazione del dataframe 
file1 = pd.read_csv("Datasets/Ordini.csv", low_memory= None,delimiter=";",on_bad_lines='skip') # lettura del csv Ordini
file2 = pd.read_csv("Datasets/PC_puliti.csv", low_memory= None,delimiter=",",on_bad_lines='skip') # lettura del csv Parametri
file3 = pd.read_csv("Datasets/BOM_per_Ordine.csv", low_memory= None,delimiter=";",on_bad_lines='skip') # lettura del csv Parametri
# Nomi delle colonne
MyName=file1.columns  
MyName1=file2.columns
MyName2=file3.columns
# Creazione dei dataframe


# creazione della tabella col sqlite3

conn = sqlite3.connect("DatabaseSql/MTD.db")  # connessione al database
cursor = conn.cursor() # creo cursore che serve per fare le azioni che seguono
# Prima funzione per la creazione della tabella Ordini con eliminazione di alcune colonne ridondanti 
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Ordini (
        Id_Ordine TEXT PRIMARY KEY,
        {MyName[0]} INTEGER,
        {MyName[1]} TEXT,
        {MyName[2]} TEXT,
        {MyName[3]} TEXT,
        {MyName[4]} TEXT,
        {MyName[5]} TEXT,
        {MyName[6]} TEXT       
      
        );
    """

)
#Seconda funzione per la creazione della
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Parametri (
        
        Id_Parametro TEXT PRIMARY KEY,
        {MyName1[1]} INTEGER REFERENCES Ordini ({MyName[0]}),
        {MyName1[2]} TEXT ,
        {MyName1[6]} TEXT ,
        {MyName1[7]} INTEGER,
        U_M CHAR(64)
        );
    """
)
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS BOM(
            Id_Bom CHAR(64),
            {MyName2[0]} REFERENCES Ordini({MyName[0]}),
            {MyName2[3]} CHAR(64),
            {MyName2[4]} CHAR(64)
        );
        
    """

)
cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Limiti (
        id_limiti INTEGER PRIMARY KEY,
        Ordine TEXT,
        Pressa TEXT,
        Tag_stampo TEXT,
        Part_number TEXT,
        Parametro TEXT, 
        Limite_inf INTEGER,
        Limite_sup INTEGER         
      
        );
        
    """

) #funzione execute per eseguire la stringa fatta li sopra al fine di creare una tabella con sei colonne, 1 id e 5 codici
# inserimento dei codici attraverso un ciclo wile 

try:
    
    for chunk1 in pd.read_csv("Datasets/Ordini.csv", chunksize=chunk_size,low_memory= None,delimiter=";",on_bad_lines='skip'):
        for index, row in chunk1.iterrows():
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO Ordini (Id_Ordine, {MyName[0]}, {MyName[1]},{MyName[2]},{MyName[3]},{MyName[4]},{MyName[5]},{MyName[6]})
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('OR'+str(index +1), row[f"{MyName[0]}"], row[f"{MyName[1]}"], row[f"{MyName[2]}"], 
                      row[f"{MyName[3]}"], row[f"{MyName[4]}"], row[f"{MyName[5]}"],row[f"{MyName[6]}"])
                )
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()
    
  
    
    for chunk2 in pd.read_csv("Datasets/PC_puliti.csv", chunksize=chunk_size,low_memory= None,delimiter=",",on_bad_lines='skip'):
        for index, row in chunk2.iterrows():
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO Parametri (Id_Parametro, {MyName1[1]}, {MyName1[2]}, {MyName1[6]},{MyName1[7]},U_M)
                    VALUES (?, ?, ?, ?,?,?)
                """, ('PAR'+str(index +1), row[f"{MyName1[1]}"], row[f"{MyName1[2]}"], row[f"{MyName1[6]}"],row[f"{MyName1[7]}"], row[f"{MyName1[9]}"])
                )
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()
    for chunk3 in pd.read_csv("Datasets/BOM_per_Ordine.csv", chunksize=chunk_size,low_memory= None,delimiter=";",on_bad_lines='skip'):
        for index, row in chunk3.iterrows():
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO BOM (Id_Bom, {MyName2[0]},{MyName2[3]},{MyName2[4]})
                    VALUES (?, ?, ?, ?)
                """, ('BOM'+str(index +1), row[f"{MyName2[0]}"], row[f"{MyName2[3]}"], row[f"{MyName2[4]}"])
                )
            except sqlite3.IntegrityError as e:
                print(f"Errore di integrità: {e} sulla riga {index}")
        conn.commit()  
except Exception as e:
    print(f"Errore durante l'importazione: {e}")
# Chiudi connessione





conn.close() # chiusura 
