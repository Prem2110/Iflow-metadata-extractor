import json
from pathlib import Path

from semantic_classifier import classify_iflow
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

deployment_id = os.getenv("LLM_DEPLOYMENT_ID")
RAW_METADATA = Path("output/metadata_raw.json")
OUTPUT_METADATA = Path("output/metadata_semantic.json")


def main():
    llm = ChatOpenAI(
        deployment_id=deployment_id,
        temperature=0,
    )

    raw_data = json.loads(RAW_METADATA.read_text())
    enriched = []

    for item in raw_data:
        print(f"🧠 Classifying: {item['iflow_name']}")

        semantic = classify_iflow(llm, item)

        enriched.append({
            **item,
            "semantic": semantic
        })

    OUTPUT_METADATA.write_text(json.dumps(enriched, indent=2))
    print(f"\n✅ Semantic metadata written to {OUTPUT_METADATA}")


if __name__ == "__main__":
    main()
