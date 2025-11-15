import pandas as pd

def read_test_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
    return df.to_dict(orient="records")
