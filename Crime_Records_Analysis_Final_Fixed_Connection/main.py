from read_clean import read_and_clean_data
from upload_mysql import upload_to_mysql
from analytics import run_analytics
from visualization import show_visualization
import pandas as pd

def add_manual_record():
    try:
        print("\n🔹 Enter new crime record details:")
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM:SS): ")
        location = input("Location: ")
        city = input("City: ")
        district = input("District: ")
        crime_type = input("Crime Type: ")
        weapon_used = input("Weapon Used: ")

        new_record = pd.DataFrame([{
            'Date': date,
            'Time': time,
            'Location': location,
            'City': city,
            'District': district,
            'Crime_Type': crime_type,
            'Weapon_Used': weapon_used
        }])
        upload_to_mysql(new_record)
    except Exception as e:
        print(f"❌ Error adding record: {e}")

def main():
    while True:
        print("\n===== Crime Records System =====")
        print("1. View cleaned data")
        print("2. Add new crime record manually")
     
        print("3. Run analytics")
        print("4. Show visualizations")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            df = read_and_clean_data('data/crime_data.csv')
            print(df.head())

        elif choice == '2':
            add_manual_record()

        elif choice == '3':
            run_analytics()

        elif choice == '4':
            df = read_and_clean_data('data/crime_data.csv')
            show_visualization(df)

        elif choice == '5':
            print("👋 Exiting...")
            break

        else:
            print("⚠️ Invalid choice. Please select a number between 1 and 5.")

if __name__ == '__main__':
    main()
