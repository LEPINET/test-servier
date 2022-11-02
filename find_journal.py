from config import JSON_GRAPH_PATH, JSON_GRAPH_NAME
import json


def get_max_occurence_journal(graph_path: str):
    with open(graph_path) as graph:
        graph_dict = json.load(graph)
        journal_reference = {}
        for drug in graph_dict:
            for journal in graph_dict[drug]["journal"]:
                if journal in journal_reference:
                    journal_reference[journal] = journal_reference[journal] + 1
                else:
                    journal_reference[journal] = 1

        max_value = 0
        max_journal = "None"
        for journal in journal_reference:
            new_value = journal_reference[journal]
            if new_value > max_value:
                max_value = new_value
                max_journal = journal
    return (max_journal, max_value)


if __name__ == "__main__":

    graph_path = JSON_GRAPH_PATH + JSON_GRAPH_NAME
    f = open("result_max_journal.txt", "a")
    f.write(str(get_max_occurence_journal(graph_path)))
    f.close()
