import logging
import os
import shutil
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import EVENT_HOMEASSISTANT_START

_LOGGER = logging.getLogger(__name__)

DOMAIN = "securlan"

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
    ("rest_command", "reload"),
]

async def reload_supported_integrations(hass: HomeAssistant):
    """Chiama i servizi di reload per le integrazioni supportate."""
    for domain, service in RELOAD_SERVICES:
        try:
            await hass.services.async_call(domain, service, blocking=True)
            _LOGGER.info("Servizio di reload chiamato: %s.%s", domain, service)
        except Exception as e:
            _LOGGER.warning("Errore durante reload %s.%s: %s", domain, service, e)


async def async_setup(hass: HomeAssistant, config: dict):
    """Setup del custom component."""

    async def create_packages_from_templates(_=None):
        """Copia o aggiorna tutti i file dalla cartella templates alla cartella packages."""
        config_path = hass.config.path("packages")
        templates_path = hass.config.path("custom_components", DOMAIN, "templates")

        if not os.path.exists(templates_path):
            _LOGGER.warning("La cartella 'templates' non è stata trovata: %s", templates_path)
            return

        if not os.path.exists(config_path):
            os.makedirs(config_path)
            _LOGGER.info("Cartella 'packages' creata: %s", config_path)
        else:
            _LOGGER.info("Cartella 'packages' già esistente: %s", config_path)

        for filename in os.listdir(templates_path):
            src_file = os.path.join(templates_path, filename)
            dst_file = os.path.join(config_path, filename)

            if os.path.isfile(src_file):
                shutil.copy(src_file, dst_file)
                _LOGGER.info("File copiato/aggiornato: %s -> %s", src_file, dst_file)

        # Ricarica i domini supportati dopo la copia
        await reload_supported_integrations(hass)

    # Creazione automatica alla partenza di Home Assistant
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, create_packages_from_templates)

    # Servizio manuale: crea/aggiorna tutti i file
    async def handle_create_service(call: ServiceCall):
        await create_packages_from_templates()
        hass.components.persistent_notification.create(
            "La cartella 'packages' è stata popolata/aggiornata dai file in 'templates'.",
            title="Custom Packages"
        )

    # Servizio manuale: copia o aggiorna un singolo file specificato
    async def handle_copy_file_service(call: ServiceCall):
        filename = call.data.get("filename")
        if not filename:
            _LOGGER.error("Parametro 'filename' mancante nel servizio copy_file")
            return

        config_path = hass.config.path("packages")
        templates_path = hass.config.path("custom_components", DOMAIN, "templates")
        src_file = os.path.join(templates_path, filename)
        dst_file = os.path.join(config_path, filename)

        if not os.path.exists(src_file):
            _LOGGER.error("Il file '%s' non esiste nella cartella templates", src_file)
            return

        if not os.path.exists(config_path):
            os.makedirs(config_path)
            _LOGGER.info("Cartella 'packages' creata: %s", config_path)

        shutil.copy(src_file, dst_file)
        _LOGGER.info("File copiato/aggiornato: %s -> %s", src_file, dst_file)

        # Ricarica i domini supportati dopo la copia
        await reload_supported_integrations(hass)

        hass.components.persistent_notification.create(
            f"File '{filename}' copiato/aggiornato nella cartella 'packages'.",
            title="Custom Packages"
        )

    # Servizio manuale: ricarica tutte le entità in packages
    async def handle_reload_packages_service(call: ServiceCall):
        await reload_supported_integrations(hass)
        hass.components.persistent_notification.create(
            "Tutti i domini supportati sono stati ricaricati dalle configurazioni in 'packages'.",
            title="Custom Packages"
        )

    # Registra i servizi
    hass.services.async_register(DOMAIN, "create_packages", handle_create_service)
    hass.services.async_register(DOMAIN, "copy_file", handle_copy_file_service)
    hass.services.async_register(DOMAIN, "reload_packages", handle_reload_packages_service)

    _LOGGER.info("Custom component '%s' caricato con successo", DOMAIN)
    return True
