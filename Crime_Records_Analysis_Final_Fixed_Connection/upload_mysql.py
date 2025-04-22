import mysql.connector
from db_config import get_connection

def upload_to_mysql(df):
    # Connect using the get_connection (which already includes crime_db)
    conn = get_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crimes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Date DATE,
            Time TIME,
            Location VARCHAR(255),
            City VARCHAR(100),
            District VARCHAR(100),
            Crime_Type VARCHAR(100),
            Weapon_Used VARCHAR(100)
        )
    """)

    # Define all expected columns
    expected_columns = ['Date', 'Time', 'Location', 'City', 'District', 'Crime_Type', 'Weapon_Used']

    # Warn about missing columns and add them as 'Unknown' or placeholder if needed
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        print(f"❌ Error: Missing columns in input data: {missing_cols}")
        print(f"ℹ️ Available columns: {list(df.columns)}")
        for col in missing_cols:
            df[col] = 'Unknown' if col != 'Time' else '00:00:00'  # default time placeholder

    # Ensure only the required columns in correct order and drop rows with missing values
    df = df[expected_columns].dropna()

    for index, row in df.iterrows():
        row_data = tuple(row)
        if len(row_data) != len(expected_columns):
            print(f"⚠️ Skipping row at index {index} due to missing data: {row_data}")
            continue
        try:
            cursor.execute("""
                INSERT INTO crimes (Date, Time, Location, City, District, Crime_Type, Weapon_Used)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, row_data)
        except Exception as e:
            print(f"❌ Failed to insert row {index}: {e}")

    conn.commit()
    print(f"✅ {len(df)} valid records uploaded to MySQL successfully.")
    cursor.close()
    conn.close()
