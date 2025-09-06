import os
import shutil
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "securlan-home_assistant"

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup del custom component."""

    package_dir = hass.config.path("packages")
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    # Crea cartella packages se non esiste
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
        _LOGGER.info("Creata cartella 'packages' in %s", package_dir)

    # Copia tutti i file YAML dalla cartella templates
    if os.path.exists(templates_dir):
        for filename in os.listdir(templates_dir):
            if filename.endswith(".yaml"):
                src_file = os.path.join(templates_dir, filename)
                dst_file = os.path.join(package_dir, filename)

                if not os.path.exists(dst_file):
                    shutil.copy(src_file, dst_file)
                    _LOGGER.info("Copiato %s in packages", filename)
                else:
                    _LOGGER.debug("Il file %s esiste già, salto", filename)
    else:
        _LOGGER.warning("La cartella templates non esiste in %s", templates_dir)

    return True

