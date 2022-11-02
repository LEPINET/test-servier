from src.processing import process_files
from src.graph_generator import generate_graph
import logging


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    logging.info("Processing files")
    process_files()

    logging.info("Generating graph")
    generate_graph()
