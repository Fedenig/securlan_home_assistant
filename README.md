# ![Logo](https://github.com/Fedenig/securlan_home_assistant/blob/main/icon.png) # securlan_home_assistant- Versione 1.0.0  

> Home Assistant / Centrali di Allarme SecurLan / Evoforce srl  

> Per gestire questa integrazione è indispensabile avere installato in centrale la scheda SmartHome.  

## Integrazione custom per Home Assistant
L'integrazione consente di popolare Home Assistant dei controlli di una centrale di allarme SecurLan per 8 Aree, 64 zone Filo, 64 Zone Radio e 64 Uscite.  
Vengono caricati gli Aiutanti che determinano la presenza delle entità di centrale ( Aree, Zone, Uscite e Diagnostica ).  
Vengono caricati tutti gli scripts per inviare alla centrale i comandi di On/Off Area, Esclusione/Inclusione Zona ed Attivazione/Disattivazione Uscita.  
Viene caricato un template di definzione personalizzata degli stati di On/Off Area, Inclusione/Esclusione, Pronta/Non Pronta, Allarme/Normale di Zona e stato Attivata/Disattivata Uscita.  
I nomi di Area, Zona Filo e Radio ed Uscita sono definiti dai file a default ma sono liberamente riprogrammabili.  
Viene caricato un file RestCommand che definisce tutti i comandi inviabili da Home Assistant alla centrale.  
Allo scopo programmare correttamente nel file secrets.yaml il valore definito al seguente punto [DIPENDENZE DI SVILUPPO](#definizione-delle-dipendenze-di-sviluppo)  

### CONTROLLO AREE - Da Home assistant verso la centrale
Ogni controllo di singola Area consente da Home Assistant l'inserimento ( ritardato, forzato, immediato o imnmediato/forzato ) ed il disinserimento.  
L'azione sulla Area è subordinabile al controllo via password con tastiera di controllo dedicata.  
La password da utilizzare sulla tastiera è definibile per codice numerico da 1 a 6 cifre.  
A tale scopo vedi sotto programmazione da inserire in file secret.yaml del vostro Home Assistant al punto [DIPENDENZE DI SVILUPPO](#definizione-delle-dipendenze-di-sviluppo)  

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

### MODULI GRAFICI:  
#### è indispensabile che nella vostra installazione di Home Assistant siano presenti il modulo HACS ed il File Editor.<br>
#### Per utilizzare la grafica degli oggetti pre-programmati ( codice.yaml e JS template ) a controllo della centrale ( On/Off Aree con tastiera e password ), Inclusione/Esclusione zona e relativo stato, Attivazione/ Disattivazione e Uscita e relativo stato è suggerita l'installazione dei seguenti moduli: 

<br>

- Bubble Card<br>
- Button Card<br> 
- Browser Mod ( installaziopne ed registrazione browser)<br>
- Custom-ui<br>
- Lovelace Card-mod<br>
- Lovelace Mushroom<br>

<br>

Dopo il download dei moduli sopra descritti aprire con il File Editor il file configuratio.yaml ed inserire i riferimenti extra_module_url: come da indicazioni sotto esposte. 

```js
# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /homeassistant/www/community/lovelace-card-mod/card-mod.js
    - /homeassistant/www/community/custom-ui/custom-ui.js
    - /homeassistant/www/community/kiosk-mode/kiosk-mode.js
    - /homeassistant/www/community/lovelace-mushroom/mushroom.js
    
```
--------------------------------------------------

# INSTALLAZIONE
#### DOWNLOAD DELLA INTEGRAZIONE TRAMITE HACS E PROCEDURA DI SETUP
In sezione HACS cliccare sui tre puntini posti in alto a destra e selezionare dalla tendina Archivi Digitali Personalizzati.  
Apparirà il popup del download.  
Inserire nel campo Archvio Digitale il seguente link: https://github.com/Fedenig/securlan_home_assistant.  
Nel campo Tipo selezionare Integrazione.  
A seguire premere AGGIUNGI.  
Il link inserito farò riferimento alla integrazione securlan-homeassistant.  
Continuare con AGGIUNGI.  
Un link con il nome della integrazione custom SecurLan verrà mostrato nella parte superiore del popup.  
L'icona cestino consente la sua rimozione in futuro. Chiudere il popup.  
Ora l'archivio HACS del vostro Home Assistant conterrà nella sua lista anche la repository SecurLan ( inserire nome in ricerca).  
Procedere con il downoload manuale della repository.  
Cliccare sui tre puntini posti sulla destra della riga della repository Securlan e dalla lista selezionare SCARICA.  
In alternativa cliccare sulla riga della repository SecurLan e dalla pagina delle info in basso a destra cliccare sul tasto SCARICA.  

### DEFINIZIONE DELLE DIPENDENZE DI SVILUPPO   

### Dopo aver effettuato il download della repository aprire con File Editor il file configuration.yaml ed inserire le seguenti informazioni.
Nel file secrets.yaml si deve definire Indirizzo IP e porta che fanno capo alla scheda SmartHome.

```js
homeassistant:
  packages: !include_dir_named packages

# API
api:
securlan:
```
--------------------------------------------------

### A seguire aprire il file secrets.yaml ed inserire le seguenti informazioni:  
Definire Indirizzo IP e porta che fanno capo alla scheda SmartHome della centrale Securlan.  
Questi dati sono fondamentali per il corretto invio di stati e comandi da Home Assistsnt alla centrale SecurLan.  
Inserire dopo **rest_command_url:** l'indirizzo IP senza http:// e la stringa fino ad action=  prelevabili dalla SmartHome,come da esempio sotto:  
- struttura,   INDIRIZZO IP:PORTA/httpr.php?key=TOKEN&action=  
- esempio,     **192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=**   

Definire la password di convalida comandi aree verso la centrale, da digitare sulla tastiera.  
Solo ammessi solo numeri con massimo di 6 cifre a vostra discrezione - default 1234  

```js
# Indirizzo IP e porta scheda SmartHome per invio stati e comandi alla centrale  
# INDIRIZZO IP:PORTA/httpr.php?key=TOKEN&action=  
# esempio: 192.168.1.100/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=  

rest_command_url: 192.168.1.100/httpr.........&action=  

# Password controllo antifurto da tastiera

password_allarme: 1234
```
--------------------------------------------------


Salvare ed a seguire portarsi su Strumenti per sviluppatori.  
Effettuare una Verifica Configurazione.  
Effettuare una ricarica di tutta la configurazione YAML.  
Effettuare un Riavvio di Home Assistant.  
Al riavvio troverete dispobili tutti gli elementi di Area, Zona Filo, Zona Radio ed Uscite ( sezione Dispositivi e Servizi / Aiutanti ).  
In sezione Automazione e Scenari saranno presenti le Automazioni e gli Script dedicati al controllo delle azioni da e verso la centrale di Allarme.  
Si suggerisce di creare una Plancia ANTIFURTO dove collocare i controlli di centrale e mostrare lo stato degli elementi di centrale.  
I dati di controllo dell'antifurto SecurLan sono stati inseriti in diversi files .yaml presenti in una nuova cartella chiamata packages.  

## NOTA IMPORTANTE: 
se al riavvio Home Assistant non avesse creato la cartella Packages e caricato al suo interno i files .yaml, portarsi su Strumenti per sviluppatori.  
Entrare in lista AZIONI. In AZIONI inserire in ricerca il testo securlan.  
Selezionata l'azione **Create Packages** (securlan.create_packages) e cliccare su **ESEGUI AZIONE**.  
Ad azione eseguita effettuare una Verifica Configurazione, una ricarica di tutta la configurazione YAML ed un Riavvio di Home Assistant.  

## PROGRAMMAZIONE PER AUTORIZZARE I COMANDI DA SECURLAN VERSO HOME ASSISTANT

Per consentire alla centrale di allarme Securlan di inviare ad Home Assistant gli stati real time delle Aree (on/off, non pronta, allarme),  delle Zone Filo e Radio (esclusa, non pronta, allarme), delle Uscite (attivata/disattivata) e della Diagnostica è necessario programmare nella scheda SmartHome l'attivazione del servizio Home Assistant.  
Dopo l'attivazione è necessario inserire le informazioni relative all'Indirizzo Ip e Porta di Home assistant ed inserire un Bearer Token a lungo termine.  
Indirizzo IP (default 'homeassistant.local') e Porta (default '8123') sono facilmente reperibili dalla sezione rete in Impostazioni.  
Per il Bearer Token, se non ancora creato e disponibile per questa integrazione, è necessario crearne uno allo scopo.  
Portarsi in sezione Generale (cliccare sulla lista di sinistra sul nome del vostro account) e poi in Sicurezza (vedi parte alta della sezione Generale).  
Sulla parte inferiore del pannello Sicurezza è presente un tasto CREA TOKEN.  
Procedere con la generazione del Token e la copia dello stesso per poi inserirlo in sezione Home Assistant della SmartHome.  
In SmartHome, una volta attivato il servizio Home Assistant, programmati Indirizzo Ip, Porta ed il Bearer Token, la centrale Securlan sarà in grado di notificare ad Home Assistant tutte le variazioni di stato relativamente ad Aree, Zone Filo e Radio, Uscite e Diagnostica.  
Da questo momento lo stato delle 8 aree, 64 zone filo, 64 zone radio e la diagnostica di base di centrale saranno costantemente in real time notificati ad Home Assistant ad ogni variazione.  

#### PERSONALIZZAZIONE GRAFICA DEI COMANDI SULLE AREE CON TASTIERA E PASSWORD, SULLE ZONE E SULLE USCITE.  

Al link **http://www.evoforce.it/homeassistant/file.zip**  
si può scaricare un file .zip che contiene in formato .txt i codici .yaml per generare gli oggetti grafici di controllo Area ( on/off ) tramite password in tastiera, zone filo, radio, uscite e diagnostica di base.  
Il file .zip contiene anche la plancia Antifurto ( codice .yaml ) con pre-programmati gli elementi di controllo delle Aree, Zone, Uscite, Diagnostica ed i Popup della tastiera grafica per il controllo del sistema di allarme SecurLan.  

<br> 

Sotto alcune immagini che mostrano il modo con cui sono stati creati i controlli da Home Assistant verso il sistema di allarme SecurLan.  
Tali files.yaml utilizzano contenuti che necessitano della presenza dei moduli descritti al punto [MODULI GRAFICI](#moduli-grafici)  
Si suggerisce di creare una Plancia ANTIFURTO dove collocare i controlli di centrale e mostrare lo stato degli elementi di centrale.  

<br> 

#### SOTTO ALCUNE IMMAGINI DI ESEMPIO PLANCIA ANTIFURTO CONTROLLI VERSO CENTRALE SECURLAN

<br> 

#### CONTROLLI CENTRALE DI ALLARME

![CONTROLLI CENTRALE DI ALLARME](https://raw.githubusercontent.com/Fedenig/securlan_home_assistant/main/assets/controlli_centrale_di_allarme.png)

<br> 

#### CONTROLLI ZONE ED USCITE

<br> 

![CONTROLLI ZONE ED USCITE](https://raw.githubusercontent.com/Fedenig/securlan_home_assistant/main/assets/controlli_zona_ed_uscita.png)

<br> 

#### CONTROLLO AREE DA TASTIERA

<br> 

![CONTROLLO AREE DA TASTIERA](https://raw.githubusercontent.com/Fedenig/securlan_home_assistant/main/assets/controllo_area_da_tastiera.png)

<br> 

#### INTEGRAZIONI MODULI DA HACS

<br> 

![INTEGRAZIONI MODULI](https://raw.githubusercontent.com/Fedenig/securlan_home_assistant/main/assets/integrazioni.png)

<br> 

#### SETUP BROWSER MOD

<br> 

![SETUP BROWSER MOD](https://raw.githubusercontent.com/Fedenig/securlan_home_assistant/main/assets/setup_pannello_browser_mod.png)

<br> 
<br> 
<br> 

