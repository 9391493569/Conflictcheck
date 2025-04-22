import pandas as pd

def read_and_clean_data(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.json'):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format")

    df.drop_duplicates(inplace=True)
    df.fillna('Unknown', inplace=True)
    return df
