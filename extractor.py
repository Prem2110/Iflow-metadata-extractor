import json
from pathlib import Path
from adapter_scanner import scan_for_adapters
from manifest_parser import parse_manifest
from identity_utils import normalize_identity
from extractor_utils import count_features, classify_complexity
from config import (
    TEMPLATE_DIR,
    EXTRACT_DIR,
    OUTPUT_DIR,
    OUTPUT_FILE
)
from extractor_utils import (
    unzip_iflow,
    scan_bpmn_for_adapters,
    detect_features,
    classify_trigger_and_payload
)


def extract_metadata(zip_path: Path):
    iflow_dir = unzip_iflow(zip_path)

    script_count, mapping_count = count_features(iflow_dir)
    complexity = classify_complexity(script_count, mapping_count)

    manifest = parse_manifest(iflow_dir)
    identity = normalize_identity(manifest, zip_path.stem)

    return {
        "template_id": identity["template_id"],
        "iflow_id": identity["iflow_id"],
        "package_id": identity["package_id"],
        "iflow_name": zip_path.stem,

        "script_count": script_count,
        "mapping_count": mapping_count,
        "complexity": complexity
    }




def main():
    EXTRACT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    all_metadata = []

    zip_files = list(TEMPLATE_DIR.glob("*.zip"))
    if not zip_files:
        print("❌ No iFlow ZIPs found in templates/")
        return

    for zip_file in zip_files:
        print(f"🔍 Processing: {zip_file.name}")
        metadata = extract_metadata(zip_file)
        all_metadata.append(metadata)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=2)

    print(f"\n✅ Metadata extraction complete")
    print(f"📄 Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
