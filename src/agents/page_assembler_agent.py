from typing import Dict, Any, List

class PageAssemblerAgent:
    """
    Assembles the final page structure from the outputs of previous agents.
    """
    def run(self, product: Dict[str, Any], questions: List[Dict[str, str]], content_blocks: Dict[str, Any], competitor: Dict[str, Any]) -> Dict[str, Any]:
        
        # Combine everything into the final JSON structure
        page = {
            "title": product.get("name"),
            "meta_description": content_blocks.get("description"),
            "product_details": product,
            "marketing_content": {
                "description": content_blocks.get("description"),
                "benefits": content_blocks.get("benefits"),
                "verdict": content_blocks.get("comparison_verdict")
            },
            "comparison": {
                "competitor_name": competitor.get("name"),
                "table": content_blocks.get("comparison_rows")
            },
            "faq": questions
        }
        
        # In a real scenario, we might have multiple pages or formats
        return {"product_page": page}
