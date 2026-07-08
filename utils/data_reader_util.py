import json
import csv
import openpyxl


def read_json_data(file_path: str):
    """
    Reads test data from a JSON file and returns a list of tuples.
    Example JSON structure:
    [
        {"email": "test1@example.com", "password": "abc123", "validity": "valid"},
        {"email": "test2@example.com", "password": "xyz123", "validity": "invalid"}
    ]
    """
    data = []
    try:
        with open(file_path, "r") as file:
            json_data = json.load(file)
        for record in json_data:
            #data.append((record["email"], record["password"], record["validity"]))
            data.append(tuple(record.values())) # Convert dictionary values to tuple (preserve order of keys)

    except FileNotFoundError as e:
        print(f"Error finding JSON file (not found): {e}")
        raise

    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        raise

    except KeyError as e:
        print(f"Missing key in JSON data: {e}")
        raise
    
    return data


def read_csv_data(file_path: str):
    """
    Reads test data from a CSV file and returns a list of tuples.
    CSV file should contain headers: email,password,validity
    """
    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                #data.append((row["email"], row["password"], row["validity"]))
                data.append(tuple(row.values()))
    
    except FileNotFoundError as e:
        print(f"Error finding csv file (not found): {e}")
        raise
    except KeyError as e:
        print(f"Missing key in csv data: {e}")
        raise
    
    return data


def read_excel_data(file_path: str, sheet_name: str = None):
    """
    Reads test data from an Excel file and returns a list of tuples.
    Assumes the first row contains headers (email, password, validity).
    """
    data = []
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name] if sheet_name else workbook.active
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
    
    except FileNotFoundError as e:
        print(f"Error finding Excel file (not found): {e}")
        raise
    except KeyError as e:
        print(f"Missing key in Excel data: {e}")
        raise
    
    return data

