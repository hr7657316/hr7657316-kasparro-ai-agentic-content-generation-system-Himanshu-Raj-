from typing import TypedDict, List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Product:
    name: str
    concentration: str
    skin_type: str
    key_ingredients: str
    benefits: str
    how_to_use: str
    side_effects: str
    price: str

    def to_dict(self):
        return asdict(self)

class AgentState(TypedDict):
    """
    Represents the state of the content generation workflow.
    """
    input_data: Dict[str, Any]
    product_model: Optional[Dict[str, Any]] # Serialized Product
    competitor_data: Optional[Dict[str, Any]]
    questions: Optional[List[Dict[str, str]]]
    content_blocks: Optional[Dict[str, Any]]
    final_pages: Optional[Dict[str, Any]]
    validation_report: Optional[str]
