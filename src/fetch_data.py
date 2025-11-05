def fetch_data():
    """
    Führt die API-Abfrage für /drucksache und /vorgang aus.
    """
    try:
        with open("config/settings.json", "r", encoding="utf-8") as config_file:
            settings = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logging.error("Konfigurationsdatei konnte nicht geladen werden: %s", exc)
        return

    auth_settings = settings.get("auth", {})
    env_var_name = auth_settings.get("env_var_name", "DIP_API_KEY")
    api_key = os.environ.get(env_var_name)
    if not api_key:
        logging.error("API-Key in Umgebungsvariable %s nicht gefunden", env_var_name)
        return

    base_url = settings.get("api_base_url", "https://search.dip.bundestag.de/api/v1")
    endpoints = settings.get("endpoints", {})
    request_params = settings.get("request_params", {}).copy()
    date_range = settings.get("date_range", {})
    raw_storage = settings.get("storage", {}).get("raw_data_path", "data/raw/")

    headers = {"Authorization": f"ApiKey {api_key}"}
    session = requests.Session()

    def try_fetch(endpoint_name, endpoint_path, base_params):
        """
        Versucht, für einen Endpunkt mehrere mögliche Datumsfilter durchzuprobieren.
        Gibt True zurück, wenn mindestens eine Variante funktioniert hat.
        """
        # Basis: immer Cursor setzen
        base_params = base_params.copy()
        base_params.setdefault("cursor", "*")

        # Kandidaten je nach Endpunkt
        candidates = []

        if endpoint_name == "drucksache":
            # Hier kennen wir die Felder sicher
            filt = {}
            if date_range.get("from"):
                filt["f.datum.start"] = date_range["from"]
            if date_range.get("to"):
                filt["f.datum.end"] = date_range["to"]
            candidates.append(("f.datum", filt))
        else:
            # Für /vorgang wissen wir nicht sicher, ob f.aktualisiert.* akzeptiert wird,
            # deshalb mehrere Varianten probieren
            if date_range:
                # 1. Versuch: aktualisiert
                filt1 = {}
                if date_range.get("from"):
                    filt1["f.aktualisiert.start"] = date_range["from"]
                if date_range.get("to"):
                    filt1["f.aktualisiert.end"] = date_range["to"]
                candidates.append(("f.aktualisiert", filt1))

                # 2. Versuch: datum
                filt2 = {}
                if date_range.get("from"):
                    filt2["f.datum.start"] = date_range["from"]
                if date_range.get("to"):
                    filt2["f.datum.end"] = date_range["to"]
                candidates.append(("f.datum", filt2))

            # 3. Fallback: ganz ohne Datumsfilter
            candidates.append(("ohne Datumsfilter", {}))

        # Jetzt die Kandidaten nacheinander durchgehen
        for label, extra_filters in candidates:
            params = base_params.copy()
            params.update(extra_filters)

            page = 1
            while True:
                try:
                    resp = session.get(
                        f"{base_url}{endpoint_path}",
                        headers=headers,
                        params=params,
                        timeout=30,
                    )
                except requests.RequestException as exc:
                    logging.error("API-Anfrage fehlgeschlagen (%s): %s", endpoint_name, exc)
                    return False

                # 400/404 → diesen Filter aufgeben, nächsten probieren
                if resp.status_code in (400, 404):
                    logging.warning(
                        "%s: Filtervariante '%s' führte zu HTTP %s – versuche nächste Variante",
                        endpoint_name,
                        label,
                        resp.status_code,
                    )
                    break  # nächste Filtervariante

                if resp.status_code == 429:
                    logging.warning("Rate Limit erreicht – erneuter Versuch in 60 Sekunden")
                    time.sleep(60)
                    continue

                if resp.status_code != 200:
                    logging.error(
                        "Unerwarteter Statuscode für %s: %s",
                        endpoint_name,
                        resp.status_code,
                    )
                    return False

                try:
                    data = resp.json()
                except json.JSONDecodeError as exc:
                    logging.error("Fehler beim Dekodieren der Antwort (%s): %s", endpoint_name, exc)
                    return False

                documents = data.get("documents", [])
                if not documents:
                    logging.info(
                        "Keine weiteren Dokumente für %s (Filter '%s') gefunden",
                        endpoint_name,
                        label,
                    )
                    break  # fertig mit diesem Filter → aber Filter war gültig
                # speichern
                timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                file_name = f"{endpoint_name}_{timestamp}_{page:04d}.json"
                save_path = os.path.join(raw_storage, endpoint_name, file_name)
                save_json(data, save_path)
                logging.info(
                    "%s: Seite %d gespeichert (%s) – Filter '%s'",
                    endpoint_name,
                    page,
                    save_path,
                    label,
                )

                next_cursor = data.get("cursor") or data.get("nextCursor")
                if not next_cursor or next_cursor == params.get("cursor"):
                    break

                params["cursor"] = next_cursor
                page += 1
                time.sleep(1)

            else:
                # sollte nie erreicht werden
                pass

            # wenn wir hier ankommen und keinen 400 hatten → diese Variante war ok
            if resp.status_code == 200:
                return True

        # keine Variante hat geklappt
        return False

    for endpoint_name, endpoint_path in endpoints.items():
        ok = try_fetch(endpoint_name, endpoint_path, request_params)
        if not ok:
            logging.error(
                "%s: Keine erfolgreiche Filtervariante gefunden, Endpunkt wird übersprungen",
                endpoint_name,
            )
