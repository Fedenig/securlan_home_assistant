NOTICE
______________________________________________________________________________________________________________________________
This is a custom integration of SecurLan alarm panel control under Home Assistant supervisor

INTEGRATION






### PROGRAMMAZIONE DA INSERIRE IN SECRET.YAML ###

# Use this file to store secrets like usernames and passwords.
# Learn more at https://www.home-assistant.io/docs/configuration/secrets/

#####################################################################################################
# Indirizzo IP e porta scheda SmartHome per invio stati e comandi alla centrale #
#### Inserire indirizzo IP e stringa fino a action= prelevati da SmartHome come da esempio sotto ####
#### 192.168.1.222/httpr.php?key=stwT2Gfwl1ftklCFP69QqqXsZmlUI3n1&action= ###
#####################################################################################################

rest_command_url: 

#####################################################################################################
### Password allarme ##
#### Inserire la password di convalida comandi aree da tastiera verso centrale ####
#### solo numeri con numero cifre a vostra discrezione - default 1234 ###

password_allarme: 1234

#####################################################################################################
### ID webhook per validare ricezione comandi json in ingresso automations  ##
#### Inserire un codice alfa numerico tipo ' -WvovUayJo0t8MF5qWVIxNMGZ ' ####
#### solo numeri con numero cifre a vostra discrezione - default 1234 ###

webhook_id_in:

#####################################################################################################
###  Password webhook per ricezione comandi dalla centrale  ###
#### Inserire un codice solo numerico tipo ' 1234554321 ' ####

password_webhook_in: 

