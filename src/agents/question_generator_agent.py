from typing import Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class Question(BaseModel):
    category: str = Field(description="Category of the question (e.g., Usage, Ingredients)")
    question: str = Field(description="The question text")
    answer: str = Field(description="The answer to the question")

class QuestionList(BaseModel):
    questions: List[Question] = Field(description="List of questions and answers")

class QuestionGeneratorAgent:
    """
    Generates FAQs based on product data using an LLM.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.parser = JsonOutputParser(pydantic_object=QuestionList)

    def run(self, product_data: Dict[str, Any]) -> List[Dict[str, str]]:
        prompt = PromptTemplate(
            template="""
            You are a customer support AI for a skincare brand.
            Based on the following product details, generate 10 frequently asked questions (FAQs) with helpful answers.
            Categorize them into: Usage, Ingredients, Benefits, Safety, General.
            
            Product Details:
            {product_data}

            {format_instructions}
            """,
            input_variables=["product_data"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser
        
        try:
            result = chain.invoke({"product_data": str(product_data)})
            return result['questions']
        except Exception as e:
            print(f"Error in QuestionGeneratorAgent: {e}")
            return []
