from typing import List, Optional

from loguru import logger
from msgspec import Struct, field

from whiteduck.modules.templates.model.util_classes import Condition


class Step(Struct):
    id: str
    type: str
    value: str | dict | list
    title: Optional[str] = None
    condition: Optional[List[Condition]] = field(default_factory=list)

    def __post_init__(self) -> None:
        logger.info(f"Initialized Step with id: {self.id}, type: {self.type}, value: {self.value}")
