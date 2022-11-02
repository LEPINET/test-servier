# path to the source files folder
SOURCE_FILE_PATH = "./data/source/"

# name of the source files (without the full path)
SOURCE_FILE_NAME = {"pubmed.json", "pubmed.csv", "drugs.csv", "clinical_trials.csv"}

# types of source documents where to find references to drugs
REFERENCES_TYPE = {"pubmed", "clinical_trials"}

# the types of source documents present
SOURCE_TYPE = {"pubmed", "clinical_trials", "drugs"}

# path to the processed files folder
PROCESSED_FILE_PATH = "./data/processed/"

# path to the graph result file folder
JSON_GRAPH_PATH = "./data/graph/"

# name of the graph file (without the full path)
JSON_GRAPH_NAME = "graph.json"

# dictionary referencing the required fields by document type (csv format)
CSV_REQUIERED_FIELD_NAMES = {
    "pubmed.csv": {"title", "date", "journal"},
    "clinical_trials.csv": {"scientific_title", "date", "journal"},
    "drugs.csv": {"drug"},
}

# where to find the presence of medication in the types of documents provided
WHERE_TO_SEARCH_DRUG_REFERENCE = {
    "pubmed": "title",
    "clinical_trials": "scientific_title",
    "drugs": "drug",
}
