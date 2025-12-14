from pathlib import Path

# Input ZIPs
TEMPLATE_DIR = Path("templates")

# Where ZIPs are extracted
EXTRACT_DIR = Path("extracted")

# Output metadata
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "metadata_raw.json"

# Adapter keyword mapping (Minimal Viable Metadata)
ADAPTER_KEYWORDS = {
    "HTTPS": ["http", "https"],
    "SFTP": ["sftp"],
    "REST": ["rest", "odata"],
    "JMS": ["jms"],
    "MAIL": ["mail"],
    "TIMER": ["timer"]
}
