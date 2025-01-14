
    const input1 = document.getElementById('codice_pressa_input');
    // Aggiungi evento di focus
    input1.addEventListener('focus', function () {
        input1.setAttribute('list', 'codice_pressa'); // Mostra le opzioni esistenti
    });

    // Aggiungi evento per rendere il campo editabile
    input1.addEventListener('input', function () {
        if (!input1.value) {
            input1.setAttribute('list', 'codice_pressa'); // Riassegna la lista se è vuoto
        }
    });   

    const input2 = document.getElementById('TAG_stampo_input');
    // Aggiungi evento di focus
    input2.addEventListener('focus', function () {
        input2.setAttribute('list', 'TAG_stampo'); // Mostra le opzioni esistenti
    });

    // Aggiungi evento per rendere il campo editabile
    input2.addEventListener('input', function () {
        if (!input2.value) {
            input2.setAttribute('list', 'TAG_stampo'); // Riassegna la lista se è vuoto
        }
    });
    const input3 = document.getElementById('part_number_input');
    // Aggiungi evento di focus
    input3.addEventListener('focus', function () {
        input3.setAttribute('list', 'part_number'); // Mostra le opzioni esistenti
    });

    // Aggiungi evento per rendere il campo editabile
    input3.addEventListener('input', function () {
        if (!input3.value) {
            input3.setAttribute('list', 'part_number'); // Riassegna la lista se è vuoto
        }
    });
    const input4 = document.getElementById('ordine_input');
    // Aggiungi evento di focus
    input4.addEventListener('focus', function () {
        input4.setAttribute('list', 'ordine'); // Mostra le opzioni esistenti
        // Trova l'elemento datalist esistente (se esiste)
        var datalist = document.getElementById('ordine');
    
        // Crea un nuovo elemento option "Tutti" se non è già presente
        var optionTutti = document.querySelector('#ordine option[value="Tutti"]');
        
        if (!optionTutti) {
            optionTutti = document.createElement('option');
            optionTutti.value = 'Tutti';
            optionTutti.textContent = 'Tutti';
            datalist.appendChild(optionTutti);
        }
    });

    // Aggiungi evento per rendere il campo editabile
    input4.addEventListener('input', function () {
        if (!input4.value) {
            input4.setAttribute('list', 'ordine'); // Riassegna la lista se è vuoto
        }
    });