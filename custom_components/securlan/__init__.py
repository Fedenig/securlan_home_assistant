import os
import shutil
import logging
import yaml
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
    
    # -------------------------------
    # 1. Crea cartella packages
    # -------------------------------
    async def async_create_packages_service(call: ServiceCall):
        packages_path = hass.config.path("packages")
        if not os.path.exists(packages_path):
            os.makedirs(packages_path)
            _LOGGER.info("Creata cartella packages in %s", packages_path)
        else:
            _LOGGER.info("Cartella packages già esistente: %s", packages_path)

    # -------------------------------
    # 2. Copia file templates -> packages
    # -------------------------------
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

    # -------------------------------
    # 3. Reload packages (copia + reload domini)
    # -------------------------------
    async def async_reload_packages_service(call: ServiceCall):
        await async_copy_file_service(call)
        _LOGGER.info("Pacchetti copiati, ricarico domini supportati...")
        services = hass.services.async_services()
        for domain, service in CANDIDATE_RELOAD_SERVICES:
            if domain in services and service in services[domain]:
                try:
                    await hass.services.async_call(domain, service, blocking=True)
                    _LOGGER.info("Ricaricato dominio: %s.%s", domain, service)
                except Exception as e:
                    _LOGGER.error("Errore reload %s.%s: %s", domain, service, e)

    # -------------------------------
    # 4. Set password
    # -------------------------------
    async def async_set_password_service(call):
        """Servizio per scrivere una password in secrets.yaml."""
        key = call.data.get("key")
        value = call.data.get("value")

        if not key or not value:
            _LOGGER.error("Chiave o valore mancanti per set_password")
            return

        try:
            secrets_path = hass.config.path("secrets.yaml")

            def _write_secret():
                import yaml
                if os.path.exists(secrets_path):
                    with open(secrets_path, "r", encoding="utf-8") as f:
                        secrets = yaml.safe_load(f) or {}
                else:
                    secrets = {}

                secrets[key] = value

                with open(secrets_path, "w", encoding="utf-8") as f:
                    yaml.dump(secrets, f, default_flow_style=False, allow_unicode=True)

            await hass.async_add_executor_job(_write_secret)

            # ✅ Notifica generica
            hass.async_create_task(
                hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "title": "securlan",
                        "message": f"Segreto '{key}' aggiornato correttamente",
                        "notification_id": f"securlan_{key}",
                    },
                )
            )

            _LOGGER.info("Password aggiornata con chiave: %s", key)

        except Exception as e:
            _LOGGER.error("Errore durante scrittura secrets.yaml: %s", e, exc_info=True)

    # -------------------------------
    # 5. Get password
    # -------------------------------
    async def async_get_password_service(call: ServiceCall):
        key = call.data.get("key")
        if not key:
            return

        secrets_path = hass.config.path("secrets.yaml")
        value = None
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                try:
                    import yaml
                    secrets = yaml.safe_load(f) or {}
                    value = secrets.get(key)
                except Exception as e:
                    _LOGGER.warning("Errore lettura secrets.yaml: %s", e)

        # 🔹 Aggiorna input_text.password_allarme_value
        try:
            await hass.services.async_call(
                "input_text",
                "set_value",
                {
                    "entity_id": "input_text.password_allarme_value",
                    "value": value if value else "",
                },
                blocking=True,
            )
        except Exception as e:
            _LOGGER.error("Errore aggiornamento input_text.password_allarme_value: %s", e)

        # 🔹 Crea notifica persistente
        message = (
            f"🔑 Password trovata per {key}: {value}"
            if value
            else f"❌ Nessuna password trovata per {key}"
        )
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {"title": "Securlan", "message": message},
        )

        _LOGGER.info("Get password eseguito: chiave=%s, valore=%s", key, value)

    # -------------------------------
    # 6. Append number a input_text
    # -------------------------------
    async def async_append_number_service(call: ServiceCall):
        entity_id = call.data.get("entity_id")
        number = call.data.get("number")
        if not entity_id or number is None:
            _LOGGER.error("entity_id o number mancanti in append_number")
            return
        current_state = hass.states.get(entity_id)
        current_value = current_state.state if current_state else ""
        new_value = current_value + str(number)
        await hass.services.async_call(
            "input_text",
            "set_value",
            {"entity_id": entity_id, "value": new_value},
            blocking=True
        )
        _LOGGER.info("Aggiornato %s → %s", entity_id, new_value)

    # -------------------------------
    # Registrazione dei servizi
    # -------------------------------
    hass.services.async_register(DOMAIN, "create_packages", async_create_packages_service)
    hass.services.async_register(DOMAIN, "copy_file", async_copy_file_service)
    hass.services.async_register(DOMAIN, "reload_packages", async_reload_packages_service)
    hass.services.async_register(DOMAIN, "set_password", async_set_password_service)
    hass.services.async_register(DOMAIN, "get_password", async_get_password_service)
    hass.services.async_register(DOMAIN, "append_number", async_append_number_service)

    _LOGGER.info("✅ Integrazione Securlan avviata con 6 servizi registrati")
    return True
