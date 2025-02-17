import pandas as pd
import numpy as np  # Per NaN

# Carica il CSV specificando il nome del file e il delimitatore corretto
df = pd.read_csv('Parametri_Critici_Ordini copy.csv', encoding='latin1', sep=';', on_bad_lines="skip")

# Funzione per separare il valore numerico e l'unità di misura o il simbolo percentuale
def separa_valore_unità(valore):
    # Se la parte numerica è "#", restituiamo NaN
    if '#' in valore:
        valore_numero = np.nan
        unita_misura = None  # Puoi decidere se mettere unita_misura a None o ''
    # Gestisci la percentuale
    elif '%' in valore:
        # Rimuovi il simbolo '%' e considera solo la parte numerica
        valore_numero = float(valore.replace('%', ''))
        unita_misura = '%'
    else:
        # Gestisci il caso di numero + spazio + unità di misura
        valore_split = valore.split()
        if len(valore_split) > 1:  # Verifica che ci sia effettivamente un'unità
            valore_numero = float(valore_split[0])
            unita_misura = valore_split[1]
        else:
            valore_numero = float(valore_split[0])
            unita_misura = ''  # In caso di solo numero
    
    return valore_numero, unita_misura

# Rimuovi eventuali spazi extra nei nomi delle colonne
df.columns = df.columns.str.strip()

# Applica la funzione alla colonna 'Valore' e crea due nuove colonne
df[['Valore', 'unità_misura']] = df['Valore'].apply(lambda x: pd.Series(separa_valore_unità(x)))

# Salva il DataFrame modificato nel CSV, sovrascrivendo il file esistente
df.to_csv('Parametri_Critici_Ordini copy.csv', index=False)

# Stampa il risultato per visualizzare le prime righe
print("DataFrame finale:")
print(df.head())



