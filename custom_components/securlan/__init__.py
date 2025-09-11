import os
import shutil
import logging
from homeassistant.core import HomeAssistant, ServiceCall

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
    """Setup del componente Securlan."""
    
    packages_path = hass.config.path("packages")
    templates_path = hass.config.path("custom_components", DOMAIN, "templates")
    
    # 1. Crea cartella packages
    async def async_create_packages_service(call: ServiceCall):
        packages_path = hass.config.path("packages")
        if not os.path.exists(packages_path):
            os.makedirs(packages_path)
            _LOGGER.info("Creata cartella packages in %s", packages_path)
        else:
            _LOGGER.info("Cartella packages già esistente: %s", packages_path)

    # 2. Copia file templates -> packages
    async def async_copy_file_service(call: ServiceCall):
        templates_path = hass.config.path("custom_components", DOMAIN, "templates")
        packages_path = hass.config.path("packages")
        if not os.path.exists(templates_path):
            _LOGGER.warning("Cartella templates non trovata: %s", templates_path)
            return
        os.makedirs(packages_path, exist_ok=True)
        for filename in os.listdir(templates_path):
            if filename.endswith(".yaml"):
                src = os.path.join(templates_path, filename)
                dst = os.path.join(packages_path, filename)
                shutil.copy(src, dst)
                _LOGGER.info("Copiato %s → %s", src, dst)

    # 3. Reload packages (copia + reload domini)
    async def async_reload_packages_service(call: ServiceCall):
        await async_copy_file_service(call)
        _LOGGER.info("Pacchetti copiati, ricarico domini supportati...")
        for domain in ["automation", "script", "scene", "input_text", "input_boolean", "input_number", "input_datetime"]:
            if domain in hass.services.async_services():
                if "reload" in hass.services.async_services()[domain]:
                    await hass.services.async_call(domain, "reload", blocking=True)
                    _LOGGER.info("Ricaricato dominio: %s", domain)

    # 4. Set password
    async def async_set_password_service(call: ServiceCall):
        key = call.data.get("key")
        value = call.data.get("value")
        if not key or not value:
            _LOGGER.error("Chiave o valore mancanti per set_password")
            return
        secrets_path = hass.config.path("secrets.yaml")
        with open(secrets_path, "a") as f:
            f.write(f"\n{key}: {value}")
        _LOGGER.info("Password aggiornata per %s", key)
        hass.components.persistent_notification.create(
            f"🔐 Password aggiornata per **{key}**", title="Securlan"
        )

    # 5. Get password
    async def async_get_password_service(call: ServiceCall):
        key = call.data.get("key")
        if not key:
            return
        secrets_path = hass.config.path("secrets.yaml")
        if not os.path.exists(secrets_path):
            return
        with open(secrets_path, "r") as f:
            for line in f.readlines():
                if line.startswith(f"{key}:"):
                    value = line.split(":", 1)[1].strip()
                    hass.components.persistent_notification.create(
                        f"🔑 Password trovata per {key}: {value}", title="Securlan"
                    )
                    return

    # 6. Append number a input_text
    async def async_append_number_service(call: ServiceCall):
        entity_id = call.data.get("entity_id")
        number = call.data.get("number")
        if not entity_id or number is None:
            _LOGGER.error("entity_id o number mancanti in append_number")
            return
        current = hass.states.get(entity_id)
        new_value = (current.state if current else "") + str(number)
        await hass.services.async_call(
            "input_text", "set_value", {"entity_id": entity_id, "value": new_value}
        )
        _LOGGER.info("Aggiornato %s → %s", entity_id, new_value)

    # Registrazione servizi
    hass.services.async_register(DOMAIN, "create_packages", async_create_packages_service)
    hass.services.async_register(DOMAIN, "copy_file", async_copy_file_service)
    hass.services.async_register(DOMAIN, "reload_packages", async_reload_packages_service)
    hass.services.async_register(DOMAIN, "set_password", async_set_password_service)
    hass.services.async_register(DOMAIN, "get_password", async_get_password_service)
    hass.services.async_register(DOMAIN, "append_number", async_append_number_service)

    _LOGGER.info("✅ Integrazione Securlan avviata con 6 servizi registrati")
    return True
