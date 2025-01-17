document.addEventListener("DOMContentLoaded", () => {
    // Elementi di input
    const pressaInput = $('#codice_pressa_input');
    const tagStampoSelecet = $('#TAG_stampo_input');

    

    // Inizializzazione di select2 sui dropdown
    pressaInput.select2({ placeholder: "Seleziona Pressa" });
    tagStampoSelecet.select2({ placeholder: "Seleziona Tag Stampo" });

    

    // Funzione per aggiornare il dropdown degli ordini
    function updateTagStampo() {
        const pressa = pressaInput.val();  // Valore del dropdown Pressa

     
    
        // Stampa per verificare i valori


    
        // Controlla se tutti i campi necessari sono stati selezionati
        if (pressa ) {
            // Esegui la richiesta AJAX per ottenere gli ordini
            $.ajax({
                url: '/api/Tag_stampo',
                data: {
                    filtro1: pressa,
      
                  
                },
                success: function(data) {
                    // Svuota il select2 degli ordini
                    tagStampoSelecet.empty();
    
                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        tagStampoSelecet.append(new Option(item.nome, item.id));
                    });
    
                    // Rende nuovamente attivo il Select2
                    tagStampoSelecet.trigger('change');
                },
                error: function(error) {
                    console.error("Errore durante il caricamento degli ordini:", error);
                }
            });
        } else {
            // Svuota il select2 se mancano i valori
            tagStampoSelecet.empty();
            tagStampoSelecet.trigger('change');
            
        }
    }
    

    // Aggiungi eventi di ascolto per i cambiamenti nei dropdown
    pressaInput.on('change', updateTagStampo);

   

    // Caricamento iniziale degli ordini (nel caso i primi 3 siano già selezionati)
    updateTagStampo();
});
