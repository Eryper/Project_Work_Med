document.addEventListener("DOMContentLoaded", () => {
    const pressaInput = document.getElementById("codice_pressa_input");
    const tagStampoDatalist = document.getElementById("TAG_stampo");

  
    // Funzione per aggiornare il datalist degli ordini
    function updateTag_stampo() {
        const pressa = pressaInput.value;

  
        // Controlla se tutti i campi necessari sono stati selezionati
        if (pressa) {
            // Esegui la richiesta al server
            fetch(`/api/Tag_stampo?filtro0=${pressa}`)
                .then(response => response.json())
                .then(data => {
                    // Svuota le opzioni esistenti
                    tagStampoDatalist.innerHTML = "";
  
                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.nome; // Usa il valore ricevuto dal server
                        tagStampoDatalist.appendChild(option);
                    });
                })
                .catch(error => console.error("Errore durante il caricamento degli TAG_Stampo:", error));
        } else {
            // Svuota il datalist se mancano valori
            tagStampoDatalist.innerHTML = "";
        }
    }
  
    // Aggiungi eventi di ascolto per i cambiamenti nei primi tre dropdown
    pressaInput.addEventListener("change", updateTag_stampo);

  });
  