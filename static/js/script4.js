document.addEventListener("DOMContentLoaded", () => {
    const pressaInput = document.getElementById("codice_pressa_input");
    const tagStampoInput = document.getElementById("TAG_stampo_input");
    const partNumberDatalist = document.getElementById("part_number");
  
    // Funzione per aggiornare il datalist degli ordini
    function updatePartNumber() {
        const pressa = pressaInput.value;
        const tagStampo = tagStampoInput.value;
        
  
        // Controlla se tutti i campi necessari sono stati selezionati
        if (pressa && tagStampo) {
            // Esegui la richiesta al server
            fetch(`/api/part_number?filtro4=${pressa}&filtro5=${tagStampo}`)
                .then(response => response.json())
                .then(data => {
                    // Svuota le opzioni esistenti
                    partNumberDatalist.innerHTML = "";
  
                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        const option = document.createElement("option");
                        option.value = item.nome; // Usa il valore ricevuto dal server
                        partNumberDatalist.appendChild(option);
                    });
                })
                .catch(error => console.error("Errore durante il caricamento degli ordini:", error));
        } else {
            // Svuota il datalist se mancano valori
            partNumberDatalist.innerHTML = "";
        }
    }
  
    // Aggiungi eventi di ascolto per i cambiamenti nei primi tre dropdown
    pressaInput.addEventListener("change", updatePartNumber);
    tagStampoInput.addEventListener("change", updatePartNumber);

  });
  