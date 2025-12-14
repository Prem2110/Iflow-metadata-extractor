import zipfile
from pathlib import Path
from config import EXTRACT_DIR, ADAPTER_KEYWORDS


def unzip_iflow(zip_path: Path) -> Path:
    """
    Unzips iFlow ZIP into extracted/<zip_name>/
    Idempotent: skips if already extracted
    """
    target_dir = EXTRACT_DIR / zip_path.stem
    if target_dir.exists():
        return target_dir

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)

    return target_dir


def scan_bpmn_for_adapters(iflow_dir: Path):
    """
    Very first-pass adapter detection.
    We refine this later.
    """
    senders = set()
    receivers = set()

    for bpmn in iflow_dir.rglob("*.bpmn"):
        try:
            content = bpmn.read_text(errors="ignore").lower()
        except Exception:
            continue

        for adapter, keywords in ADAPTER_KEYWORDS.items():
            for kw in keywords:
                if kw in content:
                    # crude heuristic for MVM
                    if "sender" in content:
                        senders.add(adapter)
                    if "receiver" in content:
                        receivers.add(adapter)

    return list(senders), list(receivers)


def detect_features(iflow_dir: Path):
    """
    Detect mappings and Groovy scripts
    """
    has_mapping = False
    has_groovy = False

    for file in iflow_dir.rglob("*"):
        name = file.name.lower()
        if "mapping" in name:
            has_mapping = True
        if name.endswith(".groovy"):
            has_groovy = True

    return has_mapping, has_groovy


def classify_trigger_and_payload(senders):
    """
    Simple rule-based classification (v1)
    """
    if "TIMER" in senders:
        return "BATCH", "MESSAGE"
    if "SFTP" in senders:
        return "ASYNC", "FILE"
    if "HTTPS" in senders or "REST" in senders:
        return "SYNC", "MESSAGE"

    return "UNKNOWN", "UNKNOWN"
def count_features(iflow_dir):
    script_count = 0
    mapping_count = 0

    for file in iflow_dir.rglob("*"):
        name = file.name.lower()
        if name.endswith(".groovy"):
            script_count += 1
        if "mapping" in name:
            mapping_count += 1

    return script_count, mapping_count


def classify_complexity(script_count, mapping_count):
    if script_count + mapping_count == 0:
        return "LOW"
    if script_count + mapping_count <= 3:
        return "MEDIUM"
    return "HIGH"
