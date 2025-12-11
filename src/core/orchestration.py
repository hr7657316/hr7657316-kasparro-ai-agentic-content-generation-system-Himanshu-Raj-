import json
import os
import logging
from typing import Dict, Any

from langgraph.graph import StateGraph, END
from .state import AgentState, Product
from ..agents.data_parser_agent import DataParserAgent
from ..agents.question_generator_agent import QuestionGeneratorAgent
from ..agents.content_logic_agent import ContentDraftingAgent
from ..agents.competitor_agent import CompetitorGenerationAgent
from ..agents.page_assembler_agent import PageAssemblerAgent
from ..agents.validation_agent import ValidationAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Manages the workflow of agents using LangGraph.
    """
    def __init__(self):
        self.data_parser = DataParserAgent()
        self.question_generator = QuestionGeneratorAgent()
        self.competitor_generator = CompetitorGenerationAgent()
        self.content_drafter = ContentDraftingAgent()
        self.page_assembler = PageAssemblerAgent()
        self.validator = ValidationAgent()
        
        self.app = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Define Nodes
        workflow.add_node("parse_data", self._node_parse_data)
        workflow.add_node("generate_questions", self._node_generate_questions)
        workflow.add_node("generate_competitor", self._node_generate_competitor)
        workflow.add_node("draft_content", self._node_draft_content)
        workflow.add_node("assemble_pages", self._node_assemble_pages)
        workflow.add_node("validate_pages", self._node_validate_pages)

        # Define Edges
        workflow.set_entry_point("parse_data")
        workflow.add_edge("parse_data", "generate_questions")
        workflow.add_edge("generate_questions", "generate_competitor")
        workflow.add_edge("generate_competitor", "draft_content")
        workflow.add_edge("draft_content", "assemble_pages")
        workflow.add_edge("assemble_pages", "validate_pages")
        workflow.add_edge("validate_pages", END)

        return workflow.compile()

    # Node Functions
    def _node_parse_data(self, state: AgentState):
        logger.info("Node: Parsing Data...")
        product_dict = self.data_parser.run(state["input_data"])
        return {"product_model": product_dict}

    def _node_generate_questions(self, state: AgentState):
        logger.info("Node: Generating Questions...")
        questions = self.question_generator.run(state["product_model"])
        return {"questions": questions}

    def _node_generate_competitor(self, state: AgentState):
        logger.info("Node: Generating Competitor...")
        competitor = self.competitor_generator.run(state["product_model"])
        return {"competitor_data": competitor}

    def _node_draft_content(self, state: AgentState):
        logger.info("Node: Drafting Content...")
        content = self.content_drafter.run(state["product_model"], state["competitor_data"])
        return {"content_blocks": content}

    def _node_assemble_pages(self, state: AgentState):
        logger.info("Node: Assembling Pages...")
        pages = self.page_assembler.run(
            state["product_model"],
            state["questions"],
            state["content_blocks"],
            state["competitor_data"]
        )
        return {"final_pages": pages}

    def _node_validate_pages(self, state: AgentState):
        logger.info("Node: Validating Pages...")
        report = self.validator.run(state["final_pages"])
        return {"validation_report": report}

    def run(self, input_file_path: str, output_dir: str) -> None:
        """
        Executes the content generation workflow.
        """
        logger.info(f"Starting orchestration with input: {input_file_path}")
        
        if not os.path.exists(input_file_path):
            logger.error(f"Input file not found: {input_file_path}")
            return

        with open(input_file_path, 'r') as f:
            raw_data = json.load(f)

        # Initial State
        initial_state = AgentState(
            input_data=raw_data,
            product_model=None,
            competitor_data=None,
            questions=None,
            content_blocks=None,
            final_pages=None,
            validation_report=None
        )

        try:
            # Run the graph
            final_state = self.app.invoke(initial_state)
            
            # Save Output
            self._save_output(final_state["final_pages"], output_dir)
            logger.info(f"Workflow completed. Validation Report: {final_state['validation_report']}")

        except Exception as e:
            logger.exception(f"An error occurred during workflow: {e}")
            raise

    def _save_output(self, pages: Dict[str, Any], output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for name, content in pages.items():
            filename = f"{name}.json"
            path = os.path.join(output_dir, filename)
            try:
                with open(path, 'w') as f:
                    json.dump(content, f, indent=2)
                logger.info(f"Saved {filename}")
            except IOError as e:
                logger.error(f"Failed to save {filename}: {e}")
