from config import (
    WHERE_TO_SEARCH_DRUG_REFERENCE,
    REFERENCES_TYPE,
    PROCESSED_FILE_PATH,
    JSON_GRAPH_PATH,
    JSON_GRAPH_NAME,
)
from src.utils import create_directories
import os
import pandas as pd
import json
import logging


def find_occurrence(reference_type: str, files: list, drug_name: str):
    """
    Find drug occurrences in a given csv file

    Parameters
    ----------
    reference_type: str
        type of the source document
    files: list
        files in the processed folder
    drug_name: str
        name of the drug

    Returns
    -------
    (DataFrame, DataFrame)
        A tuple containing a table of drug occurrences and another
        containing the data extracted from the source file
    """

    matching = [PROCESSED_FILE_PATH + file for file in files if reference_type in file]

    if matching:
        source = pd.concat(map(pd.read_csv, matching), ignore_index=True)

        find_drug = (
            source[WHERE_TO_SEARCH_DRUG_REFERENCE[reference_type]]
            .str.find(drug_name)
            .to_frame()
        )
    else:
        return (None, None)
    return (find_drug, source)


def find_add_references(drug_name: str, graph: dict):
    """
    Used to organize the retrieval of drug information and store it in the graph dictionary

    Parameters
    ----------
    drug_name: str
        name of the drug
    graph: dict
        dictionary containing all the information about drugs

    Returns
    -------
    dict
        dictionary containing all the information about drugs
    """
    entries = os.listdir(PROCESSED_FILE_PATH)

    drug = {}
    drug["journal"] = {}
    for reference_type in REFERENCES_TYPE:

        (find_drug, source) = find_occurrence(
            reference_type=reference_type, files=entries, drug_name=drug_name
        )

        drug = add_reference_type_to_drug(
            drug=drug,
            reference_type=reference_type,
            references=find_drug,
            source=source,
        )

    return add_drug_to_graph(graph=graph, drug=drug, drug_name=drug_name)


def add_drug_to_graph(graph: dict, drug: dict, drug_name: str):
    """
    Adds the information of a drug to the graph by removing the duplicate dates in the journal

    Parameters
    ----------
    graph: dict
        dictionary containing all the information about drugs
    drug: dict
        dictionary containing all informations about the drug
    drug_name: str
        name of the drug

    Returns
    -------
    dict
        dictionary containing all the information about drugs
    """
    journals = drug["journal"]
    for journal in journals:
        drug["journal"][journal] = list(set(drug["journal"][journal]))

    graph[drug_name] = drug
    return graph


def add_reference_type_to_drug(drug: dict, reference_type: str, references, source):
    """
    Adds the information of a drug from one type of reference to the drug dictionary

    Parameters
    ----------
    drug: dict
        dictionary containing the informations of the drug
    reference_type: str
        type of the source document
    references: DataFrame
        DataFrame containing the data of the source document
    source: DataFrame

    Returns
    -------
    dict
        dictionary containing all the information about drugs
    """
    lines = references.query(
        WHERE_TO_SEARCH_DRUG_REFERENCE[reference_type] + ">" + "-1"
    ).index

    drug[reference_type] = []

    for line_num in lines:
        line = source.iloc[line_num]
        date = line["date"]
        drug[reference_type].append(
            {
                "title": line[WHERE_TO_SEARCH_DRUG_REFERENCE[reference_type]],
                "date": date,
            }
        )

        if line["journal"] in drug["journal"]:
            drug["journal"][line["journal"]].append(date)
        else:
            drug["journal"][line["journal"]] = [date]

    return drug


def generate_graph():
    """
    Allows the good coordination of the functions for the creation
    of the graph and writes it in a file
    """
    create_directories(paths=[JSON_GRAPH_PATH])

    graph = {}

    drugs_csv = pd.read_csv(PROCESSED_FILE_PATH + "drugs.csv")

    for drug in drugs_csv["drug"]:
        graph = find_add_references(drug_name=drug, graph=graph)

    with open(JSON_GRAPH_PATH + JSON_GRAPH_NAME, "w") as file:
        file.write(json.dumps(graph, indent=4, ensure_ascii=False))

    logging.info("Generation of the graph successfully done")
