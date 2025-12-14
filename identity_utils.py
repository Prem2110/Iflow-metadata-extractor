def clean_symbolic_name(value: str) -> str:
    """
    Removes OSGi attributes like '; singleton:=true'
    """
    return value.split(";")[0].strip()

def normalize_identity(manifest: dict, fallback_name: str):
    raw_symbolic = manifest.get("Bundle-SymbolicName")

    if raw_symbolic:
        package_id = clean_symbolic_name(raw_symbolic)
    else:
        package_id = "unknown.package"

    iflow_id = (
        manifest.get("SAP-Integration-Flow-Id")
        or package_id.split(".")[-1]
        or fallback_name.replace(" ", "").replace("-", "")
    )

    template_id = f"{package_id}::{iflow_id}"

    return {
        "package_id": package_id,
        "iflow_id": iflow_id,
        "template_id": template_id
    }

