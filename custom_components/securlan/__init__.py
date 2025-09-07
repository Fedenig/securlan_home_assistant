import os
import shutil
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "mypackages"

def setup(hass, config):
    """Set up del custom component."""

    # Percorso cartella config di Home Assistant
    config_path = hass.config.path("packages")

    # Se la cartella non esiste, creala
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        _LOGGER.info("Creata cartella packages in %s", config_path)

    # Cartella dei file inclusi nel componente
    source_dir = os.path.join(os.path.dirname(__file__), "templates")

    if os.path.exists(source_dir):
        for filename in os.listdir(source_dir):
            src_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(config_path, filename)

            # Copia solo se il file non esiste già
            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                _LOGGER.info("File %s copiato in packages", filename)

    return True
