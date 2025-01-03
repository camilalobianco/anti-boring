import sqlite3
from api_request import get_activities
from typing import Dict

def add_new_activity_to_database(activity_data: Dict) -> bool:
    
    try:
        conn = sqlite3.connect('bored_database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                activity TEXT,
                type TEXT,
                participants INTEGER,
                price REAL,
                link TEXT,
                key TEXT PRIMARY KEY,
                accessibility REAL
            )
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO activities 
            (activity, type, participants, price, link, key, accessibility)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity_data['activity'],
            activity_data['type'],
            activity_data['participants'],
            activity_data['price'],
            activity_data['link'],
            activity_data['key'],
            activity_data['accessibility']
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding activity to database: {e}")
        return False

def fetch_and_store_new_activity(quantity: int = 1) -> bool:
    
    try:
        successes = 0
        activities = get_activities(quantity)
        
        for activity_data in activities:
            if activity_data and add_new_activity_to_database(activity_data):
                successes += 1
                
        print(f"Added {successes} out of {quantity} activities")
        return successes == quantity
        
    except Exception as e:
        print(f"Error fetching and storing activities: {e}")
        return False

if __name__ == "__main__":
    success = fetch_and_store_new_activity(5)
    print("All activities added successfully!" if success else "There were failures adding some activities.")
