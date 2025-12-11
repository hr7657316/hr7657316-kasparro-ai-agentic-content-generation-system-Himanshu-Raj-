from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

class ValidationAgent:
    """
    Validates the final generated content for quality and compliance using an LLM.
    """
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    def run(self, final_pages: Dict[str, Any]) -> str:
        prompt = PromptTemplate(
            template="""
            You are a rigorous content editor and compliance officer.
            Review the following generated product page content.
            Check for:
            1. Logical consistency (e.g. price matches).
            2. Professional tone.
            3. No prohibited claims (e.g. "cure", "guaranteed").
            
            Content:
            {content}
            
            If it passes, output "PASS".
            If there are issues, list them strictly.
            """,
            input_variables=["content"]
        )

        chain = prompt | self.llm | StrOutputParser()
        
        try:
            report = chain.invoke({"content": str(final_pages)})
            print(f"Validation Report: {report}")
            return report
        except Exception as e:
            print(f"Error in ValidationAgent: {e}")
            return "Validation Failed: Error executing validation."
