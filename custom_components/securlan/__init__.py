import os
import shutil
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "securlan"

async def async_setup(homeassistant, config):
    """Setup asincrono del componente custom."""

    try:
        config_path = homeassstant.config.path("packages")

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

        return True

    except Exception as e:
        _LOGGER.error("Errore nel setup di %s: %s", DOMAIN, e)
        return False
