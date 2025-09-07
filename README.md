# ![Logo](https://github.com/Fedenig/securlan_home_assistant/blob/main/icon.png) # securlan_home_assistant- Versione 1.0.0

> Home Assistant / Centrali di Allarme SecurLan / Evoforce srl


## Integrazione custom per Home Assistant
L'integrazione consente di popolare Home Assistant dei controlli di una centrale di allarme SecurLan per 8 Aree, 64 zone Filo, 64 Zone Radio e 64 Uscite.
Vengono caricati gli Aiutanti che determinano la presenza delle entità di centrale ( Aree, Zone, Uscite e Diagnostica ).
Vengono caricati tutti gli scripts per inviare alla centrale i comandi di On/Off Area, Esclusione/Inclusione Zona ed Attivazione/Disattivazione Uscita.
Viene caricato un template di definzione personalizzata degli stati di On/Off Area, Inclusione/Esclusione, Pronta/Non Pronta, Allarme/Normale di Zona e stato Attivata/Disattivata Uscita.
I nomi di Area, Zona Filo e Radio ed Uscita sono definiti dai file a default ma sono liberamente riprogrammabili.
Viene caricato un file RestCommand che definisce tutti i comandi inviabili da Home Assistant alla centrale.
Allo scopo programmare correttamente nel file secrets.yaml il valore definito al seguente punto [DIPENDENZE DI SVILUPPO](#programmazione-obbligatoria-da-inserire-in-file-di-sistema-secrets)

### CONTROLLO AREE - Da Home assistant verso la centrale
Ogni controllo di singola Area consente da Home Assistant l'inserimento ( ritardato, forzato, immediato o imnmediato/forzato ) ed il disinserimento.
L'azione sulla Area è subordinabile al controllo via password con tastiera di controllo dedicata.
La password da utilizzare sulla tastiera è definibile per codice numerico da 1 a 6 cifre.
A tale scopo vedi sotto programmazione da inserire in file secret.yaml del vostro Home Assistant al punto [DIPENDENZE DI SVILUPPO](#programmazione-obbligatoria-da-inserire-in-file-di-sistema-secrets)

### CONTROLLO ZONE FILO e RADIO - Da Home assistant verso la centrale
Ogni controllo di Zona Filo o Radio consente di inviare alla centrale il comando di Esclusione o Inclusione.

### CONTROLLO USCITE - Da Home assistant verso la centrale
Ogni controllo di Uscita consente di inviare alla centrale il comando di Attivazone/Disattivazione della Uscita.

### COMANDI INVIATI DALLA CENTRALE VERSO HOMEASSISTANT
Tramite API di Home Assistant, utilizzando un Bearer Token permanente, sarà possibile ricevere dalla centrale di allarme gli stati ed i comandi di Area, Zona Filo e Radio ed Uscita.
Per le Aree vengono inviati ad Home Assistant gli stati di ON e OFF.
Per le Zone Filo e Radio vengono inviati ad Home Assistant dalla centrale gli stati di Esclusione/Inclusione, Apertura/Chiusura, Allarme/Riposo.
Per le Uscite vengono inviati ad Home Assistant dalla centrale gli stati di uscita Attivata/Disattivata.
Per la Diagnostiva vengono inviati ad Home Assistant dalla centrale gli stati Rete 220V, Batteria Centrale, Tamper Centrale e Tamper Sirena.
Altri stati di diagnostica possono essere aggiunti manualmente.


## DOWNLOAD DELLA INTEGRAZIONE TRAMITE HACS
In sezione HACS cliccare sui tre puntini posti in alto a destra e selezionare dalla tendina Archivi Digitali Personalizzati.
Apparirà il popup del download.
Inserire nel campo Archvio Digitale il seguente link: https://github.com/Fedenig/securlan_home_assistant
Nel campo Tipo selezionare Integrazione.
A seguire premere AGGIUNGI.
Il link inserito farò riferimento alla integrazione securlan-homeassistant.
Continuare con AGGIUNGI.
Un link con il nome della integrazione custom SecurLan verrà mostrato nella parte superiore del popup.
L'icona cestino consente la sua rimozione in futuro. Chiudere il popup.
Ora l'archivio SecurLan apparirà nella lista delle repository di HACS.
Ora la repo deve essere scaricata. 
Cliccare sui tre puntini posti sulla destra della riga della repo Securlan e dalla lista selezionare SCARICA.
In alternativa cliccare sulla riga della integrazione SecurLan e dalla pagina delle info in basso a detra cliccare sul tasto SCARICA.
Dopo aver effettuato il download portarsi su Strumenti per sviluppatori.
Effettuare una Verifica Configurazione ed un Riavvio di Home Assistant.




## DEFINIZIONE DELLE DIPENDENZE DI SVILUPPO
Dopo avere scaricato ed avviato l'integrazione si deve procedere con la programmazion dei seguenti dati.

### PROGRAMMAZIONE OBBLIGATORIA DA INSERIRE IN FILE DI SISTEMA CONFIGURATION

```js
homeassistant:
  packages: !include_dir_named packages

# API
api:
securlan:
```

### PROGRAMMAZIONE OBBLIGATORIA DA INSERIRE IN FILE DI SISTEMA SECRETS

Nel file secrets.yaml si deve definire Indirizzo IP e porta scheda SmartHome per il corretto invio di stati e comandi alla centrale SecurLan.
Inserire dopo  rest_command_url:  l'indirizzo IP senza http:// e la stringa fino ad action=  prelevati dalla vostra SmartHome come da esempio sotto:

192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=

```js
# Indirizzo IP e porta scheda SmartHome per invio stati e comandi alla centrale
rest_command_url: INDIRIZZO IP:PORTA/httpr.php?key=token_webhook&action=
```

--------------------------------------------------

Nel file secrets.yaml si deve definire la password di convalida comandi aree da tastiera verso centrale da digitare su tastiera.
Solo ammessi solo numeri con numero massimo di 6 cifre a vostra discrezione - default 1234

```js
# Password controllo antifurto da tastiera
password_allarme: 1234
```

### PROGRAMMAZIONE DA INSERIRE IN FILE DI SISTEMA SECRETS

Nel file secrets.yaml definire l'ID webhook per validare ricezione eventuali comandi json in ingresso automations.

Inserire un codice alfa numerico tipo ' -WvovUayJo0t8MF5qWVIxNMGZ '

```js
# ID webhook per ricezione comandi dalla centrale. Da programmare in SmartHome - Homeassistant
webhook_id_in:
```

---------------------------------------------------

Nel file secrets.yaml definire la password webhook per ricezione comandi dalla centrale.

Inserire un codice solo numerico tipo ' 1234554321 '

```js
# Password webhook per ricezione comandi dalla centrale. Da programmare in SmartHome - Homeassistant
password_webhook_in: 
```




### PERSONALIZZAZIONE GRAFICA DEI COMANDI SULLE AREE CON TASTIERA E PASSWORD
Al link http://......   sono disponibili esempi dei file .yaml per ricreare i controlli di Area ( on/off ) tramite password in tastiera, zone filo, radio ed uscite.


