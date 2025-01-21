document.addEventListener("DOMContentLoaded", () => {
    // Elementi di input
    const pressaInput = $('#codice_pressa_input');
    const tagStampoSelecet = $('#TAG_stampo_input');

    // Inizializzazione di select2 sui dropdown
    pressaInput.select2({ placeholder: "Seleziona Pressa" });
    tagStampoSelecet.select2({ placeholder: "Seleziona Tag Stampo" });

    // Funzione per aggiornare il dropdown del Tag Stampo
    function updateTagStampo() {
        const pressa = pressaInput.val();  // Valore del dropdown Pressa

        // Stampa per verificare i valori
        console.log('Pressa:', pressa);

        // Controlla se il campo "Pressa" è stato selezionato
        if (pressa) {
            // Esegui la richiesta AJAX per ottenere i Tag Stampo
            $.ajax({
                url: '/api/Tag_stampo',
                data: {
                    filtro1: pressa
                },
                success: function(data) {
                    // Svuota il select2 del Tag Stampo
                    tagStampoSelecet.empty(); // Svuota il dropdown prima di aggiungere nuove opzioni

                    // Aggiungi l'opzione predefinita (Vuoto o "Seleziona Tag Stampo")
                    tagStampoSelecet.append(new Option("Seleziona Tag Stampo", ""));

                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        tagStampoSelecet.append(new Option(item.nome, item.id));
                    });

                    // Rende nuovamente attivo il Select2
                    tagStampoSelecet.trigger('change');
                },
                error: function(error) {
                    console.error("Errore durante il caricamento dei Tag Stampo:", error);
                }
            });
        } else {
            // Se "Pressa" non è selezionata, svuota il select2
            tagStampoSelecet.empty();
            tagStampoSelecet.trigger('change');
        }
    }
    
    // Aggiungi eventi di ascolto per i cambiamenti nei dropdown
    pressaInput.on('change', updateTagStampo);

    // Caricamento iniziale dei Tag Stampo (nel caso "Pressa" sia già selezionata)
    updateTagStampo();
});

