import json
from semantic_schema import SemanticMetadata


SYSTEM_PROMPT = """
You are an SAP CPI integration classifier.

You MUST return ONLY valid JSON.
You MUST follow the schema EXACTLY.
You MUST NOT add or rename fields.
You MUST choose values ONLY from the allowed enums.
You MUST include a confidence value between 0.0 and 1.0.

If unsure, use "unknown".
Do not explain anything.

Examples:

Example 1:
iFlow Name: replicate account from sap s4hana to salesforce
Output:
{
  "pattern": "replication",
  "direction": "outbound",
  "interaction": "asynchronous",
  "business_domain": "master_data",
  "confidence": 0.9
}

Example 2:
iFlow Name: get invoice pdf
Output:
{
  "pattern": "request_response",
  "direction": "inbound",
  "interaction": "synchronous",
  "business_domain": "transactional",
  "confidence": 0.85
}

Example 3:
iFlow Name: access datastore for erp
Output:
{
  "pattern": "utility",
  "direction": "internal",
  "interaction": "unknown",
  "business_domain": "integration_utility",
  "confidence": 0.8
}

"""



def build_prompt(iflow_name, script_count, mapping_count, complexity):
    hints = derive_hints(iflow_name)

    hint_text = "\n".join(f"- {h}" for h in hints) if hints else "No hints available."

    return f"""
Classify the following SAP CPI iFlow.

iFlow Name: {iflow_name}
Groovy Scripts: {script_count}
Mappings: {mapping_count}
Complexity: {complexity}

Contextual Hints:
{hint_text}

Return JSON with EXACTLY these keys:
pattern
direction
interaction
business_domain
confidence
"""


def classify_iflow(llm, raw_metadata: dict) -> SemanticMetadata:
    prompt = build_prompt(
        raw_metadata["iflow_name"],
        raw_metadata["script_count"],
        raw_metadata["mapping_count"],
        raw_metadata["complexity"]
    )

    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    result = json.loads(response.content)
    return validate_semantic_output(result)


from semantic_schema import SemanticMetadata

def validate_semantic_output(obj: dict) -> SemanticMetadata:
    required_keys = {
        "pattern",
        "direction",
        "interaction",
        "business_domain",
        "confidence"
    }

    if not required_keys.issubset(obj.keys()):
        raise ValueError(f"Invalid semantic output: {obj}")

    return obj  # typed guarantee

def derive_hints(iflow_name: str):
    name = iflow_name.lower()
    hints = []

    if any(k in name for k in ["replicate", "replication"]):
        hints.append("This iFlow looks like a data replication flow.")
    if any(k in name for k in ["get", "retrieve", "fetch"]):
        hints.append("This iFlow looks like a request-response service.")
    if any(k in name for k in ["create", "update", "delete"]):
        hints.append("This iFlow performs a transactional operation.")
    if any(k in name for k in ["datastore", "cache", "configuration"]):
        hints.append("This iFlow is an internal utility or configuration flow.")
    if any(k in name for k in ["batch", "offline", "export"]):
        hints.append("This iFlow is batch-oriented.")

    return hints
