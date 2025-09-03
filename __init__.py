import os
import shutil
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "securlan"

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup del custom component."""

    package_dir = hass.config.path("packages")

    # Crea cartella packages se non esiste
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
        _LOGGER.info("Creata cartella 'packages' in %s", package_dir)

    # Copia file YAML di esempio se non esiste già
    src_file = os.path.join(os.path.dirname(__file__), "files", "example.yaml")
    dst_file = os.path.join(package_dir, "example.yaml")

    if not os.path.exists(dst_file):
        shutil.copy(src_file, dst_file)
        _LOGGER.info("Copiato file di esempio in %s", dst_file)

    return True
