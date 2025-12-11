from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class ContentBlocks(BaseModel):
    description: str = Field(description="Marketing description of the product")
    benefits: List[str] = Field(description="List of key benefits")
    comparison_verdict: str = Field(description="Comparison verdict against competitor")
    comparison_rows: List[List[str]] = Field(description="Comparison table rows [Feature, Product, Competitor]")

class ContentDraftingAgent:
    """
    Generates marketing content and comparisons using an LLM.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.parser = JsonOutputParser(pydantic_object=ContentBlocks)

    def run(self, product_data: Dict[str, Any], competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            template="""
            You are a creative copywriter.
            Draft compelling marketing content for the following product.
            Also, create a comparison table and verdict against the competitor.
            
            Product Data:
            {product_data}
            
            Competitor Data:
            {competitor_data}

            {format_instructions}
            """,
            input_variables=["product_data", "competitor_data"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser
        
        try:
            return chain.invoke({
                "product_data": str(product_data),
                "competitor_data": str(competitor_data)
            })
        except Exception as e:
            print(f"Error in ContentDraftingAgent: {e}")
            return {}
