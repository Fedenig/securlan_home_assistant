import logging
import os
import shutil

_LOGGER = logging.getLogger(__name__)
DOMAIN = "securlan"

async def async_setup(hass, config):
    """Setup del custom component."""
    _LOGGER.info("securlan: componente caricato")

    # Percorso packages
    config_path = hass.config.path("packages")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        _LOGGER.info("Cartella packages creata in %s", config_path)

    # Copia file dalla cartella interna
    source_dir = os.path.join(os.path.dirname(__file__), "templates")
    if os.path.exists(source_dir):
        for filename in os.listdir(source_dir):
            src = os.path.join(source_dir, filename)
            dst = os.path.join(config_path, filename)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                _LOGGER.info("File %s copiato in packages", filename)
                    else:
                        _LOGGER.info("File %s già presente, non sovrascritto", filename)

            hass.bus.async_fire("securlan_copy_done")
            _LOGGER.info("Copia completata con successo.")
        except Exception as e:
            _LOGGER.error("Errore durante la copia file: %s", e)

    # Registra il servizio
    hass.services.async_register(DOMAIN, "copy_files", handle_copy_files)
    
    # Elenco dei servizi di reload supportati da HA
    RELOAD_SERVICES = [
        ("automation", "reload"),
        ("script", "reload"),
        ("input_boolean", "reload"),
        ("input_text", "reload"),
        ("input_number", "reload"),
        ("input_datetime", "reload"),
        ("group", "reload"),
        ("scene", "reload"),
    ]
    
    return True
