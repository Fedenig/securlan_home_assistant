[![Get invited](https://slack.developers.italia.it/badge.svg)](https://securlan.it/supporto/)

# securlan-homeassistant

> Home Assistant / Centrali di Allarme SecurLan / Evoforce srl

*Read this in other languages: [English](README.EN.md).*

## Come iniziare
# Integrazione custom per Home Assistant
L'integrazione consente di popolare Home Assistant dei controlli di una centrale di allarme SecurLan per 8 Aree, 64 zone Filo, 64 Zone Radio e 64 Uscite.
Vengono caricati gli Aiutanti che determinano la presenza delle entità di cenytrale ( Aree, Zone, Uscite e Diagnostica ).
Vengono caricati tutti gli scripts per inviare alla centrale i comandi di On/Off Area, Esclusione/Inclusione Zona e Attivazione/Disattivazione Uscita.
Viene caricato un template di definzione personalizzata degli stati di On/Off Area, Inclusione/Esclusione, Pronta/Non Pronta, Allarme/Normale di Zona e stato Attiva e Disattivata di Uscita.
I nomi di Area, Zona Filo e Radio ed Uscita sono definiti a default ma liberamente riprogrammabili.
Viene caricato un file Rest Command che definisce tutti i comandi inviabili da Home Assistant alla centrale.
Allo scopo programmare correttamente in file secrets.yaml il valore defino al seguente punto [DIPENDENZE DI SVILUPPO](#programmazione-obbligatoria-da-inserire-in-file-secrets)


- [Come iniziare](#come-iniziare)

### CONTROLLOAREE
Ogni controllo di singola Area consente da Home Assitant l'inserimento ( ritardato, forzato, immediato o imnmediato/forzato ) ed il disinserimento.
L'azione sulla Area è subordinata al controllo via password con tastiera di controllo dedicata.
La password da utilizzare sulla tastiera è definibile per codice numerico da 1 a 6 cifre.
A tale scopo vedi sotto programmazione da inserire in file secret.yaml del vostro Home Assistant.

### CONTROLLO ZONE FILO e RADIO
Ogni controllo di Zona Filo o Radio consente di inviare alla centrale il comando di Esclusione o Inclusione.

Tramite API di Home Assistant, utilizzando un Bearer Token permanente, sarà possibile ricevere dalla centrale di allarme gli stati ed i comandi di Area, Zona Filo e Radio ed Uscita.
Per le Aree vengono inviati ad Home Assistant gli stati di ON e OFF.
Per le Zone Filo e Radio vengono inviati ad Home Assistant dalla centrale gli stati di Esclusione/Inclusione, Apertura/Chiusura, Allarme/Riposo.

### CONTROLLO USCITE
Per le Uscite vengono inviati ad Home Assistant dalla centrale gli stati di uscita Attivata/Disattivata.
Peer la Diagnostiva vengono inviati ad Home Assistant dalla centrale gli stati Rete 220V, Batteria Centrale, Tamper Centrale e Tamper Sirena.
Altri stati di diagnostica possono essere aggiunti manualmente.


## INSTALLARE LE SEGUENTI DIPENDENZE DI SVILUPPO

### PROGRAMMAZIONE OBBLIGATORIA DA INSERIRE IN FILE CONFIGURATIONS (.yaml)

```js
homeassistant:
  packages: !include_dir_named packages

# API
api:
```

### PROGRAMMAZIONE OBBLIGATORIA DA INSERIRE IN FILE SECRETS (.yaml)

Indirizzo-IP e porta scheda SmartHome per invio stati e comandi alla centrale SecurLan.
Inserire dopo  rest_command_url:  l'indirizzo IP senza http:// e la stringa fino ad action=  prelevati dalla vostra SmartHome come da esempio sotto:

192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=

```js
rest_command_url: indirizzo ip/httpr.php?key=token_webhook&action=
```

--------------------------------------------------

Password allarme da digitare su tastiera

Inserire la password di convalida comandi aree da tastiera verso centrale

Solo numeri con numero massimo di 6 cifre a vostra discrezione - default 1234

```js
password_allarme: 1234
```

### PROGRAMMAZIONE DA INSERIRE IN FILE SECRETs (.yaml)

ID webhook per validare ricezione eventuali comandi json in ingresso automations.

Inserire un codice alfa numerico tipo ' -WvovUayJo0t8MF5qWVIxNMGZ '

```js
webhook_id_in:
```

---------------------------------------------------

Password webhook per ricezione comandi dalla centrale.

Inserire un codice solo numerico tipo ' 1234554321 '

```js
password_webhook_in: 
```



# Manutenzione 

## Licenza 



## IMMAGINI

![Recordit GIF](http://g.recordit.co/iLN6A0vSD8.gif)


# INDICE

- [Come iniziare](#come-iniziare)
- [Manutenzione](#manutenzione)
- [Licenza](#licenza)



