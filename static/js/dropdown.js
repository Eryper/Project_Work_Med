document.addEventListener("DOMContentLoaded", () => {
    const pressaInput = $('#codice_pressa_input');
    const tagStampoInput = $('#TAG_stampo_input');
    const partNumberInput = $('#part_number_input');

    pressaInput.select2({ placeholder: "Seleziona Pressa" });
    tagStampoInput.select2({ placeholder: "Seleziona Tag Stampo" });
    partNumberInput.select2({ placeholder: "Seleziona Part Number" });

    let lastFilters = {}; // Memorizza l'ultimo stato dei filtri

    function fetchData(endpoint, filters, targetSelect) {
        const selectedValue = targetSelect.val(); // Salva il valore selezionato

        $.ajax({
            url: endpoint,
            data: filters,
            success: function(data) {
                targetSelect.empty().append(new Option("Seleziona un'opzione", ""));

                data.forEach(item => {
                    const option = new Option(item.nome, item.id);
                    targetSelect.append(option);
                });

                targetSelect.val(selectedValue); // Ripristina la selezione SENZA trigger('change')
            },
            error: function(error) {
                console.error("Errore durante il caricamento dei dati:", error);
            }
        });
    }

    function updateDropdowns() {
        const pressa = pressaInput.val();
        const tagStampo = tagStampoInput.val();
        const partNumber = partNumberInput.val();

        const newFilters = { filtro1: pressa, filtro2: tagStampo, filtro3: partNumber };

        // Se i filtri sono uguali ai precedenti, non fare nulla
        if (JSON.stringify(newFilters) === JSON.stringify(lastFilters)) return;
        lastFilters = newFilters; // Aggiorna lo stato

        if (pressa || tagStampo || partNumber) {
            fetchData('/api/Tag_stampo', newFilters, tagStampoInput);
            fetchData('/api/part_number', newFilters, partNumberInput);
            fetchData('/api/pressa', newFilters, pressaInput);
        }
    }

    pressaInput.on('change', updateDropdowns);
    tagStampoInput.on('change', updateDropdowns);
    partNumberInput.on('change', updateDropdowns);

    updateDropdowns();
});


