import csv
import ast
import os
import logging


def json_to_csv(
    jsonfile_name: str,
    jsonfile_path: str,
    output_path: str,
    requiered_field_names: dict,
):
    """
    Create a csv file from a source file in json format containing tabular data

    Parameters
    ----------
    jsonfile_name: str
        name of the json file
    jsonfile_path: str
        path of the folder where to get the json file
    output_path: str
        path of the folder where to put the new csv file
    requiered_field_names: dict
        requiered field names of the tabular data

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    try:
        with open(output_path, "w") as csvfile:
            with open(jsonfile_path) as f:
                data = ast.literal_eval(f.read())
                field_names = [key for key in data[0]]
                if not requiered_field_names[
                    jsonfile_name.replace(".json", ".csv")
                ].issubset(set(field_names)):
                    print(
                        'JSON file "%s" not having requiered field names'
                        % jsonfile_name
                    )
                    return False
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(data)
        logging.info('Successfully convert "%s" to CSV' % jsonfile_name)
        return True

    except:
        message = 'Json file "%s" is not a tabular format' % jsonfile_name
        logging.error(message)
        return False


def check_csv_field_names(file_name: str, file_path: str, requiered_field_names: dict):
    """
    Check that the columns necessary to use the csv file are present

    Parameters
    ----------
    file_name: str
        name of the csv file
    file_path: str
        path to the folder containing the file
    requiered_field_names: dict
        requiered field names of the tabular data

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)

            if not requiered_field_names[file_name].issubset(reader.fieldnames):
                logging.error(
                    'CSV file "%s" does not have the required fields' % file_name
                )
                return False
            logging.info('File "%s" contains the required fields' % file_name)

    except Exception as e:
        logging.error(str(e))
        return False

    return True


def create_directories(paths: list):
    """
    Create the directories whose paths are specified

    Parameters
    ----------
    paths: list
        list of string, the paths of the folders

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    if not paths:
        logging.error("Can't create a void directory")
        return False

    for path in paths:
        if not type(path) == type(""):
            logging.error("Folder name has to be a string, given: %s" % type(path))
            return False

        if not os.path.isdir(path):
            os.mkdir(path)

    return True
