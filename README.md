# Integrazione custom per Home Assistant

# securlan-homeassistant

> Home Assistant / Centrali di Allarme SecurLan / Evoforce srl

*Read this in other languages: [English](README.EN.md).*


## Nota:

Questa è una integrazione custom per integrare in Home Assistant il controllo delle centrali di allarme SecurLan prodotte da Evoforce srl.

## Procedura per l'integrazione:

E' necessario 



## PROGRAMMAZIONE DA INSERIRE IN FILE CONFIGURATION.YAML DI HOMEASSISTANT

```js
homeassistant:
  packages: !include_dir_named packages

# API
api:
```

## PROGRAMMAZIONE DA INSERIRE IN FILE SECRET.YAML DI HOMEASSISTANT

###################################################################

Indirizzo IP e porta scheda SmartHome per invio stati e comandi alla centrale SecurLan.
Inserire dopo  rest_command_url:  l'indirizzo IP senza http:// e la stringa fino ad action=  prelevati dalla vostra SmartHome come da esempio sotto:

192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=
####################################################################

rest_command_url: indirizzo ip/httpr.php?key=token_webhook&action=

####################################################################

Password allarme da digitare su tastiera

Inserire la password di convalida comandi aree da tastiera verso centrale

Solo numeri con numero massimo di 6 cifre a vostra discrezione - default 1234
####################################################################

password_allarme: 1234

####################################################################

ID webhook per validare ricezione comandi json in ingresso automations

Inserire un codice alfa numerico tipo ' -WvovUayJo0t8MF5qWVIxNMGZ '
####################################################################

webhook_id_in:

#####################################################################

Password webhook per ricezione comandi dalla centrale

Inserire un codice solo numerico tipo ' 1234554321 '
#####################################################################

password_webhook_in: 


[![License](https://img.shields.io/github/license/italia/bootstrap-italia.svg)](https://github.com/italia/bootstrap-italia/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/italia/bootstrap-italia.svg)](https://github.com/italia/bootstrap-italia/issues)
[![Join the #design channel](https://img.shields.io/badge/Slack%20channel-%23design-blue.svg)](https://developersitalia.slack.com/messages/C7VPAUVB3/)
[![Get invited](https://slack.developers.italia.it/badge.svg)](https://slack.developers.italia.it/)
[![18app on forum.italia.it](https://img.shields.io/badge/Forum-18app-blue.svg)](https://forum.italia.it/c/18app-carta-docente)

# Annunci / Status del progetto

# Titolo

> Sottotitolo / Slogan / Descrizione breve

*Read this in other languages: [English](README.EN.md).*

## Immagini e GIF

![Recordit GIF](http://g.recordit.co/iLN6A0vSD8.gif)

# Indice

- [Come iniziare](#come-iniziare)
- [Come contribuire](#come-contribuire)
- [Manutenzione](#manutenzione)
- [Licenza](#licenza)

# Come iniziare

## Dipendenze

## Come installare

```js
console.log("Questo è un esempio di blocco di codice")
```

## Documentazione
### Link a documentazione esterna 

# Come contribuire

## Installare le dipendenze di sviluppo

## Struttura del progetto

## Community

### Code of conduct

### Responsible Disclosure

### Segnalazione bug e richieste di aiuto

# Manutenzione 

# Licenza 

## Licenza generale 

## Autori e Copyright

## Licenze software dei componenti di terze parti



