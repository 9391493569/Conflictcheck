import matplotlib.pyplot as plt
import pandas as pd
from db_config import get_connection

def run_analytics():
    conn = get_connection()
    cursor = conn.cursor()

    # Most Common Crime Types
    cursor.execute("SELECT crime_type, COUNT(*) as count FROM crimes GROUP BY crime_type ORDER BY count DESC LIMIT 5")
    results = cursor.fetchall()
    if results:
        crime_types, counts = zip(*results)
        print("\n--- Most Common Crime Types ---")
        for row in results:
            print(row)
        plt.figure(figsize=(8,5))
        plt.bar(crime_types, counts, color='skyblue')
        plt.title("Top 5 Most Common Crime Types")
        plt.xlabel("Crime Type")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("most_common_crimes.png")
        plt.close()

    # Night-Time Crimes
    cursor.execute("SELECT COUNT(*) FROM crimes WHERE time >= '20:00' OR time <= '04:00'")
    print("\n--- Night-Time Crimes (8PM - 4AM) ---")
    print("Count:", cursor.fetchone()[0])

    # Crime Hotspots
    cursor.execute("SELECT city, COUNT(*) as count FROM crimes GROUP BY city ORDER BY count DESC LIMIT 5")
    results = cursor.fetchall()
    if results:
        cities, city_counts = zip(*results)
        print("\n--- Crime Hotspots by City ---")
        for row in results:
            print(row)
        plt.figure(figsize=(8,5))
        plt.bar(cities, city_counts, color='orange')
        plt.title("Top 5 Crime Hotspots by City")
        plt.xlabel("City")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig("crime_hotspots.png")
        plt.close()

    # Arrest Rate by Weapon (if arrested column exists)
    try:
        cursor.execute("""
            SELECT weapon_used, 
                   ROUND(SUM(arrested)/COUNT(*) * 100, 2) as arrest_rate
            FROM crimes
            GROUP BY weapon_used
            ORDER BY arrest_rate DESC
        """)
        results = cursor.fetchall()
        if results:
            weapons, rates = zip(*results)
            print("\n--- Arrest Rate by Weapon Type ---")
            for row in results:
                print(row)
            plt.figure(figsize=(8,5))
            plt.bar(weapons, rates, color='green')
            plt.title("Arrest Rate by Weapon Type")
            plt.xlabel("Weapon Used")
            plt.ylabel("Arrest Rate (%)")
            plt.tight_layout()
            plt.savefig("arrest_rate_by_weapon.png")
            plt.close()
    except Exception as e:
        print("\n⚠️ Skipping 'Arrest Rate by Weapon' because the 'arrested' column doesn't exist.")

    # Seasonal Crime Variation
    cursor.execute("""
        SELECT MONTH(date) as month, COUNT(*) FROM crimes
        GROUP BY month
        ORDER BY month
    """)
    results = cursor.fetchall()
    if results:
        months, month_counts = zip(*results)
        print("\n--- Seasonal Crime Variation ---")
        for row in results:
            print(row)
        plt.figure(figsize=(8,5))
        plt.plot(months, month_counts, marker='o', linestyle='-', color='purple')
        plt.title("Seasonal Crime Variation")
        plt.xlabel("Month")
        plt.ylabel("Number of Crimes")
        plt.xticks(range(1,13))
        plt.tight_layout()
        plt.savefig("seasonal_crime_variation.png")
        plt.close()

    cursor.close()
    conn.close()
