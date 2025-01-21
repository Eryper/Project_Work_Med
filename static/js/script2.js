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
    ordineSelect.select2({ placeholder: "Seleziona Ordine", allowClear: true });

    // Variabile per tenere traccia dell'animazione di caricamento
    let loadingInterval;
    let loadingText = "Caricamento"; // Testo di base

    // Funzione per aggiornare il dropdown degli ordini
    function updateOrdine() {
        const pressa = pressaInput.val();  // Valore del dropdown Pressa
        const tagStampo = tagStampoInput.val();  // Valore del dropdown Tag Stampo
        const partNumber = partNumberInput.val();  // Valore del dropdown Part Number

        // Verifica se i dati necessari sono selezionati
        if (pressa && tagStampo && partNumber) {
            // Mostra un messaggio di caricamento con animazione dei punti
            ordineSelect.prop('disabled', true);  // Disabilita il dropdown
            ordineSelect.empty();  // Svuota le opzioni esistenti
            ordineSelect.append(new Option(loadingText, "loading")); // Aggiungi "Caricamento." iniziale

            // Inizia l'animazione dei punti
            loadingInterval = setInterval(() => {
                if (loadingText.length < 14) {
                    loadingText += "."; // Aggiungi un punto
                } else {
                    loadingText = "Caricamento"; // Reset a "Caricamento" con 0 punti
                }
                // Aggiorna l'opzione di caricamento nel select
                ordineSelect.empty();
                ordineSelect.append(new Option(loadingText, "loading"));
                ordineSelect.trigger('change');
            }, 450); // Cambia ogni 500ms

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

                    // Aggiungi un'opzione di "Tutti" come prima scelta
                    ordineSelect.append(new Option("Tutti", "Tutti"));

                    // Aggiungi nuove opzioni ricevute dal server
                    data.forEach(item => {
                        ordineSelect.append(new Option(item.nome, item.id));
                    });

                    // Rende nuovamente attivo il Select2
                    ordineSelect.prop('disabled', false); // Abilita il dropdown
                    ordineSelect.trigger('change');

                    // Ferma l'animazione di caricamento
                    clearInterval(loadingInterval);
                },
                error: function(error) {
                    console.error("Errore durante il caricamento degli ordini:", error);
                    ordineSelect.prop('disabled', false); // Abilita il dropdown anche in caso di errore

                    // Ferma l'animazione di caricamento
                    clearInterval(loadingInterval);
                }
            });
        } else {
            // Se non ci sono selezioni, svuota il select2
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




