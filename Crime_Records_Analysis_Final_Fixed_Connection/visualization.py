
import matplotlib.pyplot as plt
import pandas as pd

def show_visualization(df):
    print("Available columns:", df.columns.tolist())

    # Try to find a date-like column
    date_column = None
    for col in df.columns:
        if 'date' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if df[col].notna().sum() > 0:
                    date_column = col
                    break
            except Exception as e:
                print(f"Error parsing column {col} as date: {e}")

    if date_column:
        df = df[df[date_column].notna()]  # Drop rows where date is NaT
        counts_by_date = df[date_column].value_counts().sort_index()
        counts_by_date.plot(kind='bar', figsize=(12, 6), color='salmon')
        plt.title('Number of Crimes per Date')
        plt.xlabel('Date')
        plt.ylabel('Number of Incidents')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No suitable date column found for date-based visualization.")
