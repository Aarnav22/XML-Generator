import pandas as pd

def read_policy_numbers_from_excel(file_path, column_name='PolicyNumber'):
    try:
        df = pd.read_excel(file_path)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the Excel file.")
        return df[column_name].dropna().astype(str).str.strip().tolist()
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []
