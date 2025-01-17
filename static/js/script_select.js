$(document).ready(function() {
    // Inizializza Select2 per tutti i dropdown
    $('#TAG_stampo_input').select2({
        placeholder: "Seleziona Tag Stampo",
        allowClear: true
    });

    $('#codice_pressa_input').select2({
        placeholder: "Seleziona Pressa",
        allowClear: true
    });
    $('#ordine_input').select2({
        placeholder: "Seleziona Part Number",
        allowClear: true
    });
    $('#part_number_input').select2({
        placeholder: "Seleziona Ordine",
        allowClear: true
    });
});