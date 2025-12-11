from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from ..core.models import Product

class ProductSchema(BaseModel):
    name: str = Field(description="Name of the product")
    concentration: str = Field(description="Concentration of key ingredients")
    skin_type: str = Field(description="Recommended skin type")
    key_ingredients: str = Field(description="Key ingredients list")
    benefits: str = Field(description="Main benefits of the product")
    how_to_use: str = Field(description="Usage instructions")
    side_effects: str = Field(description="Potential side effects")
    price: str = Field(description="Price of the product")

class DataParserAgent:
    """
    Uses an LLM to parse and structure raw input data into a standardized Product model.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.parser = JsonOutputParser(pydantic_object=ProductSchema)

    def run(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            template="""
            You are an expert data analyst for skincare products.
            Extract relevant product information from the following raw data and structure it exactly according to the schema.
            If a field is missing, infer a reasonable default or mark as "Not specified".
            Ensure the tone is professional.

            Raw Data:
            {raw_data}

            {format_instructions}
            """,
            input_variables=["raw_data"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser
        
        try:
            result = chain.invoke({"raw_data": str(raw_data)})
            # Return as a dict that matches the Product dataclass
            return result
        except Exception as e:
            # Fallback or error handling
            print(f"Error in DataParserAgent: {e}")
            raise e
