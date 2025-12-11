from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class CompetitorProduct(BaseModel):
    name: str = Field(description="Name of the competitor product")
    ingredients: str = Field(description="Key ingredients of the competitor")
    benefits: str = Field(description="Benefits of the competitor product")
    price: str = Field(description="Price of the competitor product")

class CompetitorGenerationAgent:
    """
    Generates a fictional competitor product for comparison purposes using an LLM.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.9)
        self.parser = JsonOutputParser(pydantic_object=CompetitorProduct)

    def run(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            template="""
            You are a market research analyst.
            Based on the following product, create a FICTIONAL competitor product that targets the same audience but has slightly different features/price.
            Ensure the competitor is realistic.

            Target Product:
            {product_data}

            {format_instructions}
            """,
            input_variables=["product_data"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser
        
        try:
            return chain.invoke({"product_data": str(product_data)})
        except Exception as e:
            print(f"Error in CompetitorGenerationAgent: {e}")
            return {}
