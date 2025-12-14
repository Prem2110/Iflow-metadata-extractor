from pathlib import Path


def parse_manifest(iflow_dir: Path) -> dict:
    manifest_path = iflow_dir / "META-INF" / "MANIFEST.MF"

    if not manifest_path.exists():
        return {}

    metadata = {}

    with open(manifest_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    return metadata
