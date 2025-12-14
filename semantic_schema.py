from typing import Literal, TypedDict


class SemanticMetadata(TypedDict):
    pattern: Literal[
        "replication",
        "request_response",
        "batch_processing",
        "event_driven",
        "utility",
        "configuration",
        "unknown"
    ]
    direction: Literal[
        "inbound",
        "outbound",
        "bidirectional",
        "internal",
        "unknown"
    ]
    interaction: Literal[
        "synchronous",
        "asynchronous",
        "batch",
        "unknown"
    ]
    business_domain: Literal[
        "master_data",
        "transactional",
        "finance",
        "logistics",
        "integration_utility",
        "unknown"
    ]
    confidence: float
