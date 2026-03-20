from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Order:
    items: list
    total: float
    timestamp: datetime = field(default_factory=datetime.now)