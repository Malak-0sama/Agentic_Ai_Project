from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentState:
    
    dataset: Any = None

    cleaned_dataset: Any = None

    schema: Dict = field(default_factory=dict)

    plan: Dict = field(default_factory=dict)

    model_info: Dict = field(default_factory=dict)

    trained_model: Any = None

    metrics: Dict = field(default_factory=dict)

    report: Dict = field(default_factory=dict)

    logs: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)