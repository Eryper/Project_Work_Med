document.addEventListener("DOMContentLoaded", () => {
  const pressaInput = document.getElementById("codice_pressa_input");
  const tagStampoInput = document.getElementById("TAG_stampo_input");
  const partNumberInput = document.getElementById("part_number_input");

  const ordineDatalist = document.getElementById("ordine");

  // Funzione per aggiornare il datalist degli ordini
  function updateOrdini() {
      const pressa = pressaInput.value;
      const tagStampo = tagStampoInput.value;
      const partNumber = partNumberInput.value;

      // Controlla se tutti i campi necessari sono stati selezionati
      if (pressa && tagStampo && partNumber) {
          // Esegui la richiesta al server
          fetch(`/api/ordine?filtro1=${pressa}&filtro2=${tagStampo}&filtro3=${partNumber}`)
              .then(response => response.json())
              .then(data => {
                  // Svuota le opzioni esistenti
                  ordineDatalist.innerHTML = "";

                  // Aggiungi nuove opzioni ricevute dal server
                  data.forEach(item => {
                      const option = document.createElement("option");
                      option.value = item.nome; // Usa il valore ricevuto dal server
                      ordineDatalist.appendChild(option);
                  });
              })
              .catch(error => console.error("Errore durante il caricamento degli ordini:", error));
      } else {
          // Svuota il datalist se mancano valori
          ordineDatalist.innerHTML = "";
      }
  }

  // Aggiungi eventi di ascolto per i cambiamenti nei primi tre dropdown
  pressaInput.addEventListener("change", updateOrdini);
  tagStampoInput.addEventListener("change", updateOrdini);
  partNumberInput.addEventListener("change", updateOrdini);
});
