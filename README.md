# NOTA:

Questa è una integrazione custom per integrare in Home Assistant il controllo delle centrali di allarme SecurLan prodotte da Evoforce srl.

# INTEGRAZIONE

E' necessario 



# PROGRAMMAZIONE DA INSERIRE IN FILE CONFIGURATION.YAML DI HOMEASSISTANT

homeassistant:
  packages: !include_dir_named packages

api:



# PROGRAMMAZIONE DA INSERIRE IN FILE SECRET.YAML DI HOMEASSISTANT

###################################################################

Indirizzo IP e porta scheda SmartHome per invio stati e comandi alla centrale SecurLan.
Inserire dopo  rest_command_url:  l'indirizzo IP senza http:// e la stringa fino ad action=  prelevati dalla vostra SmartHome come da esempio sotto:

192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action=
####################################################################

rest_command_url: indirizzo ip/httpr.php?key=token_webhook&action=

####################################################################

Password allarme da digitare su tastiera
Inserire la password di convalida comandi aree da tastiera verso centrale ##
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


