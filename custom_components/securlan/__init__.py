import os
import shutil
import logging
from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)
DOMAIN = "securlan"

# Domini che possono essere ricaricati senza riavvio completo
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

    # -------------------------------
    # 1) Crea cartella packages
    # -------------------------------
    async def async_create_packages_service(call: ServiceCall | None = None):
        packages_path = hass.config.path("packages")
        if not os.path.exists(packages_path):
            os.makedirs(packages_path, exist_ok=True)
            _LOGGER.info("Creata cartella packages in %s", packages_path)
        else:
            _LOGGER.info("Cartella packages già esistente: %s", packages_path)

    # -------------------------------
    # 2) Copia file templates -> packages
    # -------------------------------
    async def async_copy_file_service(call: ServiceCall | None = None):
        templates_path = hass.config.path("custom_components", DOMAIN, "templates")
        packages_path = hass.config.path("packages")

        if not os.path.exists(templates_path):
            _LOGGER.warning("Cartella templates non trovata: %s", templates_path)
            return

        os.makedirs(packages_path, exist_ok=True)

        copied = 0
        for filename in os.listdir(templates_path):
            if filename.endswith(".yaml"):
                src = os.path.join(templates_path, filename)
                dst = os.path.join(packages_path, filename)
                shutil.copy(src, dst)
                copied += 1
                _LOGGER.info("📂 Copiato %s → %s", src, dst)

        if copied == 0:
            _LOGGER.info("Nessun file .yaml trovato in %s", templates_path)
        else:
            _LOGGER.info("Totale file copiati: %d", copied)

    # -------------------------------
    # 3) Reload packages (copia + reload domini)
    # -------------------------------
    async def async_reload_packages_service(call: ServiceCall | None = None):
        # Crea la cartella se manca e copia i template
        await async_create_packages_service()
        await async_copy_file_service()

        # Ricarico i domini supportati
        _LOGGER.info("Ricarico domini supportati…")
        services = hass.services.async_services()
        for domain, service in CANDIDATE_RELOAD_SERVICES:
            if domain in services and service in services[domain]:
                try:
                    await hass.services.async_call(domain, service, blocking=True)
                    _LOGGER.info("✅ Ricaricato: %s.%s", domain, service)
                except Exception as e:
                    _LOGGER.error("❌ Errore reload %s.%s: %s", domain, service, e)

    # -------------------------------
    # 4) Set password (gestita su input_text)
    # -------------------------------
    async def async_set_password_service(call: ServiceCall):
        key = call.data.get("key")          # es. "password_allarme" (solo informativo)
        value = call.data.get("value")      # il valore da salvare

        if not value:
            _LOGGER.error("Valore mancante per set_password")
            return

        try:
            await hass.services.async_call(
                "input_text",
                "set_value",
                {
                    "entity_id": "input_text.password_allarme",
                    "value": value,
                },
                blocking=True,
            )
            _LOGGER.info("Password aggiornata (key=%s, value=%s)", key, value)
        except Exception as e:
            _LOGGER.error("Errore aggiornamento input_text.password_allarme: %s", e)

    # -------------------------------
    # 5) Get password (da input_text)
    # -------------------------------
    async def async_get_password_service(call: ServiceCall):
        state = hass.states.get("input_text.password_allarme")
        value = state.state if state else ""

        message = f"🔑 Password attuale: {value}" if value else "❌ Nessuna password impostata"
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {"title": "Securlan", "message": message},
        )
        _LOGGER.info("Get password eseguito → %s", value)

    # -------------------------------
    # 6) Append number a input_text (keypad)
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
            blocking=True,
        )
        _LOGGER.info("Aggiornato %s → %s", entity_id, new_value)

    # -------------------------------
    # 7) Servizio unico: copy + reload (richiamabile anche a mano)
    # -------------------------------
    async def async_copy_and_reload_service(call: ServiceCall):
        await async_reload_packages_service()

    # -------------------------------
    # Registrazione servizi
    # -------------------------------
    hass.services.async_register(DOMAIN, "create_packages", async_create_packages_service)
    hass.services.async_register(DOMAIN, "copy_file", async_copy_file_service)
    hass.services.async_register(DOMAIN, "reload_packages", async_reload_packages_service)
    hass.services.async_register(DOMAIN, "set_password", async_set_password_service)
    hass.services.async_register(DOMAIN, "get_password", async_get_password_service)
    hass.services.async_register(DOMAIN, "append_number", async_append_number_service)
    hass.services.async_register(DOMAIN, "copy_and_reload", async_copy_and_reload_service)

    # -------------------------------
    # 8) Azione automatica all’avvio: copia + reload
    # -------------------------------
    try:
        await async_reload_packages_service()
        _LOGGER.info("📦 Template copiati e domini ricaricati automaticamente all’avvio.")
    except Exception as e:
        _LOGGER.error("Errore nella copia/ricarica automatica all’avvio: %s", e)

    _LOGGER.info("✅ Integrazione Securlan avviata (servizi attivi: create/copy/reload, set/get password, append_number)")
    return True
