import os
import shutil
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "securlan"

async def async_setup(hass, config):
    """Setup asincrono del componente custom."""
    hass.states.async_set(f"{DOMAIN}.status", "ok")

    async def handle_copy_files(call):
        """Gestisce la chiamata al servizio per copiare i file."""
        try:
            config_path = hass.config.path("packages")
            if not os.path.exists(config_path):
                os.makedirs(config_path)
                _LOGGER.info("Creata cartella packages in %s", config_path)

            source_dir = os.path.join(os.path.dirname(__file__), "templates")

            if os.path.exists(source_dir):
                for filename in os.listdir(source_dir):
                    src_file = os.path.join(source_dir, filename)
                    dest_file = os.path.join(config_path, filename)

                    if not os.path.exists(dest_file):
                        shutil.copy2(src_file, dest_file)
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
