import os
import shutil
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "securlan"

# Domini candidati al reload (solo se disponibili nei servizi di HA)
CANDIDATE_RELOAD_SERVICES = [
    ("automation", "reload"),
    ("script", "reload"),
    ("input_boolean", "reload"),
    ("input_text", "reload"),
    ("input_number", "reload"),
    ("input_datetime", "reload"),
    ("scene", "reload"),
    ("rest_command", "reload"),
]


async def async_setup(hass: HomeAssistant, config: dict):
    """Setup del componente custom."""

    async def async_create_packages_service(call):
        """Servizio manuale: crea la cartella packages se non esiste."""
        packages_path = hass.config.path("packages")
        try:
            if not os.path.exists(packages_path):
                _LOGGER.info("Creo cartella packages in %s", packages_path)
                await hass.async_add_executor_job(os.makedirs, packages_path)
            else:
                _LOGGER.info("Cartella packages già esistente: %s", packages_path)
        except Exception as e:
            _LOGGER.error("Errore durante creazione packages: %s", e, exc_info=True)

    async def async_copy_templates_to_packages(hass: HomeAssistant):
        """Copia i file dalla cartella templates a packages."""
        templates_path = hass.config.path("custom_components", DOMAIN, "templates")
        packages_path = hass.config.path("packages")

        try:
            _LOGGER.info("Inizio copia templates da %s a %s", templates_path, packages_path)

            # Creazione cartella packages se non esiste
            if not os.path.exists(packages_path):
                _LOGGER.info("Creo cartella packages")
                await hass.async_add_executor_job(os.makedirs, packages_path)

            # Lista file in templates
            try:
                filenames = await hass.async_add_executor_job(os.listdir, templates_path)
            except FileNotFoundError:
                _LOGGER.error("Cartella templates non trovata: %s", templates_path)
                return

            for filename in filenames:
                if filename.endswith(".yaml"):
                    src = os.path.join(templates_path, filename)
                    dst = os.path.join(packages_path, filename)

                    def _copy():
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy(src, dst)

                    _LOGGER.info("Copio %s → %s", src, dst)
                    await hass.async_add_executor_job(_copy)

            _LOGGER.info("Copia templates completata")

        except Exception as e:
            _LOGGER.error("Errore durante copia templates: %s", e, exc_info=True)

    async def async_reload_supported_domains(hass: HomeAssistant):
        """Ricarica i domini che supportano reload."""
        try:
            _LOGGER.info("Avvio reload domini supportati...")
            services = hass.services.async_services()
            reloaded = []

            for domain, service in CANDIDATE_RELOAD_SERVICES:
                if domain in services and service in services[domain]:
                    try:
                        _LOGGER.info("Ricarico %s.%s", domain, service)
                        await hass.services.async_call(domain, service, blocking=True)
                        reloaded.append(f"{domain}.{service}")
                    except Exception as e:
                        _LOGGER.error("Errore durante reload %s.%s: %s", domain, service, e)

            if reloaded:
                _LOGGER.info("Domini ricaricati: %s", reloaded)
            else:
                _LOGGER.info("Nessun dominio ricaricato")

        except Exception as e:
            _LOGGER.error("Errore durante reload domini: %s", e, exc_info=True)

    async def async_copy_file_service(call):
        """Servizio manuale: copia solo i file in packages."""
        _LOGGER.info("Servizio copy_file avviato")
        await async_copy_templates_to_packages(hass)

    async def async_reload_packages_service(call):
        """Servizio manuale: copia + reload domini."""
        _LOGGER.info("Servizio reload_packages avviato")
        try:
            await async_copy_templates_to_packages(hass)
            await async_reload_supported_domains(hass)
            _LOGGER.info("Servizio reload_packages completato con successo")
        except Exception as e:
            _LOGGER.error("Errore in reload_packages: %s", e, exc_info=True)

    # Registra i servizi
    hass.services.async_register(DOMAIN, "create_packages", async_create_packages_service)
    hass.services.async_register(DOMAIN, "copy_file", async_copy_file_service)
    hass.services.async_register(DOMAIN, "reload_packages", async_reload_packages_service)

    _LOGGER.info("Componente %s caricato correttamente", DOMAIN)
    return True
