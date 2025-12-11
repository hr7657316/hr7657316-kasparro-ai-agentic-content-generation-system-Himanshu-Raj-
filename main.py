import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.orchestration import Orchestrator

def setup_logging():
    """Configures the logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the application."""
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="Kasparro AI Agentic Content Generation System")
    parser.add_argument("--input", "-i", default="data/input_product.json", help="Path to input JSON file")
    parser.add_argument("--output", "-o", default="output", help="Directory for output files")
    
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle relative paths
    input_path = args.input if os.path.isabs(args.input) else os.path.join(base_dir, args.input)
    output_dir = args.output if os.path.isabs(args.output) else os.path.join(base_dir, args.output)
    
    logger.info(f"Input path: {input_path}")
    logger.info(f"Output directory: {output_dir}")

    orchestrator = Orchestrator()
    try:
        orchestrator.run(input_path, output_dir)
    except Exception as e:
        logger.critical(f"Application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
