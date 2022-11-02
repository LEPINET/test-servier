from config import (
    SOURCE_FILE_PATH,
    SOURCE_FILE_NAME,
    SOURCE_TYPE,
    PROCESSED_FILE_PATH,
    CSV_REQUIERED_FIELD_NAMES,
    WHERE_TO_SEARCH_DRUG_REFERENCE,
)
import os
import pandas as pd
import shutil
import logging
from src.utils import create_directories, json_to_csv, check_csv_field_names


def process_json(file_name: str):
    """
    Function used to process a file in json format. Checks the conformity
    of the table fields and converts the file to csv format.

    Parameters
    ----------
    file_name: str
        name of the json file

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    jsonfile_path = SOURCE_FILE_PATH + file_name
    if not os.path.isfile(jsonfile_path):
        print(f'File "%s" not found' % file_name)
        return False
    output_name = file_name.replace(".json", "_converted.csv")
    output_path = PROCESSED_FILE_PATH + output_name
    if not json_to_csv(
        jsonfile_name=file_name,
        jsonfile_path=jsonfile_path,
        output_path=output_path,
        requiered_field_names=CSV_REQUIERED_FIELD_NAMES,
    ):
        return False

    return True


def process_csv(file_name: str):
    """
    Function used to process a file in csv format. Checks the conformity of the table fields.

    Parameters
    ----------
    file_name: str
        name of the json file

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    file_path = SOURCE_FILE_PATH + file_name
    if not check_csv_field_names(
        file_name=file_name,
        file_path=file_path,
        requiered_field_names=CSV_REQUIERED_FIELD_NAMES,
    ):
        return False
    else:
        output_path = PROCESSED_FILE_PATH + file_name
        shutil.copy2(file_path, output_path)
        return True


def lower_case_column_csv():
    """
    Lower the text of the column needed to find the information
    """
    entries = os.listdir(PROCESSED_FILE_PATH)

    for source_type in SOURCE_TYPE:
        matching = [
            PROCESSED_FILE_PATH + file for file in entries if source_type in file
        ]

        if matching:
            df = pd.concat(map(pd.read_csv, matching), ignore_index=True)

            df[WHERE_TO_SEARCH_DRUG_REFERENCE[source_type]] = df[
                WHERE_TO_SEARCH_DRUG_REFERENCE[source_type]
            ].str.lower()

            for matching_file in matching:
                os.remove(matching_file)

            df.to_csv(PROCESSED_FILE_PATH + source_type + ".csv")


def process_files():
    """
    Function used to process files. it calls all the functions necessary
    for the processing of the files

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    if not create_directories(paths=[PROCESSED_FILE_PATH]):
        return False

    for file in SOURCE_FILE_NAME:
        if ".json" in file:
            if not process_json(file_name=file):
                return False
            logging.info('Successfully processed "%s"' % file)
        elif ".csv" in file:
            if not process_csv(file):
                return False
            logging.info('Successfully processed "%s"' % file)

    lower_case_column_csv()

    return True
