import logging
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv

DOMAIN = "securlan"
_LOGGER = logging.getLogger(__name__)

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

SET_PASSWORD_SCHEMA = vol.Schema({
    vol.Required("key"): cv.string,
    vol.Required("value"): cv.string,
})

GET_PASSWORD_SCHEMA = vol.Schema({
    vol.Required("key"): cv.string,
})

COPY_FILE_SCHEMA = vol.Schema({
    vol.Required("source"): cv.string,
    vol.Required("destination"): cv.string,
})

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup del dominio Securlan."""

    async def async_set_password(call: ServiceCall):
        key = call.data["key"]
        value = call.data["value"]
        hass.states.async_set(f"{DOMAIN}.{key}", value)
        hass.components.persistent_notification.create(
            f"Password {key} aggiornata.",
            title="🔐 Securlan"
        )
        _LOGGER.info("Password impostata per %s", key)

    async def async_get_password(call: ServiceCall):
        key = call.data["key"]
        state = hass.states.get(f"{DOMAIN}.{key}")
        value = state.state if state else "Nessuna password trovata"
        hass.components.persistent_notification.create(
            f"Password trovata per {key}: {value}",
            title="🔐 Securlan"
        )
        _LOGGER.info("Richiesta password per %s", key)

    async def async_reload_packages(call: ServiceCall):
        await hass.services.async_call("homeassistant", "reload_config")
        hass.components.persistent_notification.create(
            "Pacchetti ricaricati.",
            title="📦 Securlan"
        )

    async def async_copy_file(call: ServiceCall):
        src = call.data["source"]
        dst = call.data["destination"]
        try:
            with open(src, "r") as fsrc, open(dst, "w") as fdst:
                fdst.write(fsrc.read())
            hass.components.persistent_notification.create(
                f"File copiato da {src} a {dst}.",
                title="📄 Securlan"
            )
        except Exception as e:
            hass.components.persistent_notification.create(
                f"Errore copia file: {e}",
                title="⚠️ Securlan"
            )
            _LOGGER.error("Errore copia file: %s", e)

    async def async_create_packages(call: ServiceCall):
        import os
        pkg_dir = hass.config.path("packages")
        if not os.path.exists(pkg_dir):
            os.makedirs(pkg_dir)
            hass.components.persistent_notification.create(
                "Cartella packages creata.",
                title="📦 Securlan"
            )
        else:
            hass.components.persistent_notification.create(
                "Cartella packages già esistente.",
                title="📦 Securlan"
            )

    async def async_delete_password(call: ServiceCall):
        key = call.data["key"]
        hass.states.async_remove(f"{DOMAIN}.{key}")
        hass.components.persistent_notification.create(
            f"Password {key} eliminata.",
            title="🔐 Securlan"
        )
        _LOGGER.info("Password eliminata per %s", key)

    # Registra i servizi
    hass.services.async_register(DOMAIN, "set_password", async_set_password, schema=SET_PASSWORD_SCHEMA)
    hass.services.async_register(DOMAIN, "get_password", async_get_password, schema=GET_PASSWORD_SCHEMA)
    hass.services.async_register(DOMAIN, "reload_packages", async_reload_packages)
    hass.services.async_register(DOMAIN, "copy_file", async_copy_file, schema=COPY_FILE_SCHEMA)
    hass.services.async_register(DOMAIN, "create_packages", async_create_packages)
    hass.services.async_register(DOMAIN, "delete_password", async_delete_password, schema=GET_PASSWORD_SCHEMA)

        _LOGGER.info("Componente %s caricato correttamente", DOMAIN)

    return True

