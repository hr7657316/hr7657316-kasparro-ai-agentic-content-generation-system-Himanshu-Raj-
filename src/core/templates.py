import json
from typing import Dict, Any, List
import re

class TemplateEngine:
    """
    A simple template engine that replaces {{placeholders}} with data.
    Supports simple logic like loops if we were building a complex one, 
    but for this assignment, we'll keep it to structured JSON templates 
    where fields can be populated by agents.
    """
    
    def render(self, template: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively render a dictionary template using the context.
        """
        if isinstance(template, dict):
            return {k: self.render(v, context) for k, v in template.items()}
        elif isinstance(template, list):
            return [self.render(item, context) for item in template]
        elif isinstance(template, str):
            return self._replace_placeholders(template, context)
        else:
            return template

    def _replace_placeholders(self, text: str, context: Dict[str, Any]) -> Any:
        """
        Replaces {{ key }} with value from context.
        If the value is not a string (e.g. list or dict), and the text is ONLY the placeholder,
        return the object directly.
        """
        # Check if text is exactly a placeholder like "{{ key }}"
        match = re.fullmatch(r"\{\{\s*([\w\.]+)\s*\}\}", text)
        if match:
            key = match.group(1)
            val = self._get_value(key, context)
            return val if val is not None else text

        # Otherwise do string replacement
        def replace(match):
            key = match.group(1)
            val = self._get_value(key, context)
            return str(val) if val is not None else match.group(0)
        
        return re.sub(r"\{\{\s*([\w\.]+)\s*\}\}", replace, text)

    def _get_value(self, key: str, context: Dict[str, Any]) -> Any:
        """
        Retrieve value from context using dot notation (e.g. "product.name").
        """
        parts = key.split('.')
        current = context
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

# Define Templates
FAQ_TEMPLATE = {
    "page_title": "FAQ - {{ product.name }}",
    "meta_description": "Frequently asked questions about {{ product.name }}.",
    "sections": [
        {
            "heading": "Common Questions",
            "q_and_a": "{{ questions }}" 
        }
    ]
}

PRODUCT_PAGE_TEMPLATE = {
    "title": "{{ product.name }}",
    "price": "{{ product.price }}",
    "description": "{{ content_blocks.description }}",
    "benefits_list": "{{ content_blocks.benefits }}",
    "usage_instructions": "{{ product.how_to_use }}",
    "ingredients_highlight": "{{ product.key_ingredients }}"
}

COMPARISON_PAGE_TEMPLATE = {
    "title": "{{ product.name }} vs {{ competitor.name }}",
    "comparison_table": {
        "headers": ["Feature", "{{ product.name }}", "{{ competitor.name }}"],
        "rows": "{{ content_blocks.comparison_rows }}"
    },
    "verdict": "{{ content_blocks.comparison_verdict }}"
}
