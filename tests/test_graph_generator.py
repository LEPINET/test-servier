import pandas as pd
import sys, os
from unittest.mock import MagicMock

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.graph_generator import (
    add_drug_to_graph,
    add_reference_type_to_drug,
    find_occurrence,
)


def test_add_drug_to_graph():

    graph = {
        "drug1": {
            "journal": {"journal1": ["11/11/1111", "11/11/11111"]},
            "pubmed": {"pubmed_test1": "11/11/1111"},
            "clinical_trials": {"clini_test2": "11/11/1111"},
        }
    }
    drug = {
        "journal": {"journal2": ["01/01/2000"]},
        "pubmed": {"pubmed_test2": "22/22/2222"},
        "clinical_trials": {"clini_test2": "22/22/2222"},
    }
    drug_name = "drug2"
    expected_graph = {
        "drug1": {
            "journal": {"journal1": ["11/11/1111", "11/11/11111"]},
            "pubmed": {"pubmed_test1": "11/11/1111"},
            "clinical_trials": {"clini_test2": "11/11/1111"},
        },
        "drug2": {
            "journal": {"journal2": ["01/01/2000"]},
            "pubmed": {"pubmed_test2": "22/22/2222"},
            "clinical_trials": {"clini_test2": "22/22/2222"},
        },
    }
    assert expected_graph == add_drug_to_graph(
        graph=graph, drug=drug, drug_name=drug_name
    )


def test_add_reference_type_to_drug():
    drug = {
        "journal": {"journal1": ["01/01/2000"]},
        "clinical_trials": [{"clini_test": "22/22/2222"}],
    }
    reference_type = "pubmed"
    occurence = {"title": [-1, -1, 8, 6]}
    source = {
        "title": ["false", "false", "true1", "true2"],
        "journal": ["wrong", "wrong", "good1", "good2"],
        "date": ["00/00/0000", "00/00/0000", "11/11/1111", "22/22/2222"],
    }
    occurence = pd.DataFrame(occurence)
    source = pd.DataFrame(source)

    expected_drug = {
        "journal": {
            "journal1": ["01/01/2000"],
            "good1": ["11/11/1111"],
            "good2": ["22/22/2222"],
        },
        "pubmed": [
            {"title": "true1", "date": "11/11/1111"},
            {"title": "true2", "date": "22/22/2222"},
        ],
        "clinical_trials": [{"clini_test": "22/22/2222"}],
    }

    updated_drug = add_reference_type_to_drug(
        drug=drug,
        reference_type=reference_type,
        references=occurence,
        source=source,
    )

    assert expected_drug == updated_drug


def test_find_occurrence():
    source = {
        "title": ["false", "false", "true1", "atrue2"],
        "journal": ["wrong", "wrong", "good1", "good2"],
        "date": ["00/00/0000", "00/00/0000", "11/11/1111", "22/22/2222"],
    }
    mock_source = pd.DataFrame(source)
    pd.concat = MagicMock()
    pd.concat.return_value = mock_source
    (find_drug, _) = find_occurrence("pubmed", ["pubmed"], "true")
    expected_occurences = pd.DataFrame.to_dict(pd.DataFrame({"title": [-1, -1, 0, 1]}))

    assert pd.DataFrame.to_dict(find_drug) == expected_occurences
