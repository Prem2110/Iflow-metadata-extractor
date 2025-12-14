# IFLOW METADATA EXTRACTOR
METADATA Extractor for PIPO to SAP Integration Suite Migration.
Or Call it as Template Registry

## Structure
```pgsql
iflow-metadata-extractor/
│
├── extractor.py                   # run this code first, for extracting raw json from iflow zip's 
├── extractor_utils.py             # helper file
├── semantic_classifier.py         # helper file
├── semantic_schema.py             # helper file
├── adapter_scanner.py             # helper file
├── config.py                      # helper file
├── identity_utils.py              # helper file
├── manifest_parser.py             # helper file
├── enrich_metadata.py             # run this code second, llm will extract properly
│
├── output/
│   ├── metadata_raw.json          # from extractor.py
│   └── metadata_semantic.json     # enriched from llm. from enrich_metadata.py
```

### Steps
- Create: `uv init`
- Initialise venv: `uv venv .venv`
- Activate: `venv\Scripts\Activate`
- Install dependency: `uv add -r requirements.txt`

## Background Story
```java 
Local Machine (150 ZIPs)
        ↓
Python Extractor (Deterministic)
        ↓
Raw Metadata JSON
        ↓
LLM Enricher
        ↓
Template Registry
```
---
### Pros
- ✅ Accurate
- ✅ Repeatable
- ✅ No hallucination
- ✅ Fully automatable
- ✅ Works for 150 or 1,500 templates
---
### Phase 1 — Deterministic Extraction
- Parse all 150 iFlow ZIPs
- Extract:
    - Sender adapter(s)
    - Receiver adapter(s)
    - Known steps
- Produce raw machine metadata

📌 Output = boring but correct JSON

### Phase 2 — LLM Enrichment
- Feed raw metadata to LLM
- Searchable templates by pattern
- LLM-grounded intent matching
- No dependency on CPI internals
- Safe, explainable metadata
- This will help llm:
    - Template selection
    - Prompt grounding

📌 LLM never touches CPI internals directly

---
### What happens if you run only `extractor.py`
When you run: 
`extractor.py`

We will get deterministic, technical metadata only:
What you already have now:
- template_id (canonical, from MANIFEST.MF)
- package_id
- iflow_id
- script_count
- mapping_count
- complexity

*** This data is: ***
- 100% reliable
- No LLM involved
- Sufficient for cataloging, governance, packaging


### What `enrich_metadata.py` adds
- It does NOT replace extractor output. It augments it with semantic intelligence.
- It adds this block

```json
"semantic": {
  "pattern": "replication",
  "direction": "outbound",
  "interaction": "asynchronous",
  "business_domain": "master_data",
  "confidence": 0.9
}
```
This layer is what enables:
- “User says: replicate business partner”
- System says: use this template
- Intent → template matching
- Your future iFlow designer experience
 📌 Without enrich_metadata.py, the system is technical but not intelligent.

 ![alt text](image.png)

---
Exact rule
🔁 Run `extractor.py`
- When templates change
- When you add/remove iFlow ZIPs
- When you want fresh technical metadata

🧠 Run `enrich_metadata.py`
- When you want intent-based selection
- When you improve prompts / rules
- When building the “AI iFlow Designer”
They are deliberately decoupled.
---