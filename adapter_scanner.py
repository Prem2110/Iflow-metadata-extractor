from pathlib import Path

# Canonical SAP CPI adapter IDs
KNOWN_ADAPTER_IDS = {
    "sap.http": "HTTPS",
    "sap.https": "HTTPS",
    "sap.sftp": "SFTP",
    "sap.ftp": "FTP",
    "sap.soap": "SOAP",
    "sap.odata": "ODATA",
    "sap.jms": "JMS",
    "sap.mail": "MAIL",
    "sap.timer": "TIMER",
    "sap.idoc": "IDOC"
}


def scan_for_adapters(iflow_dir: Path):
    """
    Scan ALL XML files for known adapter IDs.
    Returns a set of adapter types found.
    """
    found_adapters = set()

    for xml_file in iflow_dir.rglob("*.xml"):
        try:
            content = xml_file.read_text(errors="ignore").lower()
        except Exception:
            continue

        for adapter_id, adapter_name in KNOWN_ADAPTER_IDS.items():
            if adapter_id in content:
                found_adapters.add(adapter_name)

    return list(found_adapters)
