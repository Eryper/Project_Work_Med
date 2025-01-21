document.addEventListener("DOMContentLoaded", () => {
    // Elementi di input
    const pressaInput = $('#codice_pressa_input');
    const tagStampoInput = $('#TAG_stampo_input');
    const partNumberSelect = $('#part_number_input');
    
    // Inizializzazione di select2 sui dropdown
    pressaInput.select2({ placeholder: "Seleziona Pressa" });
    tagStampoInput.select2({ placeholder: "Seleziona Tag Stampo" });
    partNumberSelect.select2({ placeholder: "Seleziona Part Number" });
    
    // Funzione per aggiornare il dropdown degli Part Number
    function updatePartnumber() {
        const pressa = pressaInput.val();  // Valore del dropdown Pressa
        const tagStampo = tagStampoInput.val();  // Valore del dropdown Tag Stampo

        // Stampa per verificare i valori
        console.log('Pressa:', pressa);
        console.log('Tag Stampo:', tagStampo);

        // Controlla se tutti i campi necessari sono stati selezionati
        if (pressa && tagStampo) {
            // Esegui la richiesta AJAX per ottenere gli Part Number
            $.ajax({
                url: '/api/part_number',
                data: {
                    filtro1: pressa,
                    filtro2: tagStampo
                },
                success: function(data) {
                    // Svuota il select2 degli Part Number
                    partNumberSelect.empty(); // Svuota il dropdown prima di aggiungere nuove opzioni

                    // Aggiungi l'opzione predefinita (Vuoto o "Seleziona Part Number")
                    partNumberSelect.append(new Option("Seleziona Part Number", ""));

                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        partNumberSelect.append(new Option(item.nome, item.id));
                    });

                    // Rende nuovamente attivo il Select2
                    partNumberSelect.trigger('change');
                },
                error: function(error) {
                    console.error("Errore durante il caricamento dei Part Number:", error);
                }
            });
        } else {
            // Se non ci sono selezioni, svuota il select2
            partNumberSelect.empty();
            partNumberSelect.trigger('change');
        }
    }
    
    // Aggiungi eventi di ascolto per i cambiamenti nei dropdown
    pressaInput.on('change', updatePartnumber);
    tagStampoInput.on('change', updatePartnumber);

    // Caricamento iniziale degli Part Number (nel caso i primi 2 siano già selezionati)
    updatePartnumber();
});


  