document.addEventListener("DOMContentLoaded", () => {
    // Elementi di input
    const pressaInput = $('#codice_pressa_input');
    const tagStampoInput = $('#TAG_stampo_input');
    const partNumberInput = $('#part_number_input');
    const ordineSelect = $('#ordine_input');

    // Inizializzazione di select2 sui dropdown
    pressaInput.select2({ placeholder: "Seleziona Pressa" });
    tagStampoInput.select2({ placeholder: "Seleziona Tag Stampo" });
    partNumberInput.select2({ placeholder: "Seleziona Part Number" });
    ordineSelect.select2({ placeholder: "Seleziona Ordine" });

    // Funzione per aggiornare il dropdown degli ordini
    function updateOrdine() {
        const pressa = pressaInput.val();  // Valore del dropdown Pressa
        const tagStampo = tagStampoInput.val();  // Valore del dropdown Tag Stampo
        const partNumber = partNumberInput.val();  // Valore del dropdown Part Number
    
        // Stampa per verificare i valori
        console.log('Pressa:', pressa);
        console.log('Tag Stampo:', tagStampo);
        console.log('Part Number:', partNumber);
    
        // Controlla se tutti i campi necessari sono stati selezionati
        if (pressa && tagStampo && partNumber) {
            // Esegui la richiesta AJAX per ottenere gli ordini
            $.ajax({
                url: '/api/ordine',
                data: {
                    filtro1: pressa,
                    filtro2: tagStampo,
                    filtro3: partNumber
                },
                success: function(data) {
                    // Svuota il select2 degli ordini
                    ordineSelect.empty();
                    ordineSelect.append(new Option("Tutti", "Tutti"));
                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        ordineSelect.append(new Option(item.nome, item.id));
                        
                        
                    });
    
                    // Rende nuovamente attivo il Select2
                    ordineSelect.trigger('change');
                },
                error: function(error) {
                    console.error("Errore durante il caricamento degli ordini:", error);
                }
            });
        } else {
            // Svuota il select2 se mancano i valori
            ordineSelect.empty();
            ordineSelect.trigger('change');
        }
    }
    

    // Aggiungi eventi di ascolto per i cambiamenti nei dropdown
    pressaInput.on('change', updateOrdine);
    tagStampoInput.on('change', updateOrdine);
    partNumberInput.on('change', updateOrdine);

    // Caricamento iniziale degli ordini (nel caso i primi 3 siano già selezionati)
    updateOrdine();
});