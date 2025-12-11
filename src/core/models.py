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
