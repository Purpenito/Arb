from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RuntimeState:
    collector_status: str = "starting"
    adapter_status: dict[str, str] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


runtime_state = RuntimeState()
