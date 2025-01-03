import sqlite3
from api_request import get_activities

def create_activities_table(connection):
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        key TEXT PRIMARY KEY,
        activity TEXT NOT NULL,
        type TEXT,
        participants INTEGER,
        price REAL,
        link TEXT,
        accessibility REAL
    )
    """)
    
    connection.commit()

def create_database():
    try:
        connection = sqlite3.connect('bored_database.db')
        create_activities_table(connection)
        print("Database e tabela criados com sucesso!")
        return connection
        
    except sqlite3.Error as e:
        print(f"Erro ao criar banco de dados: {e}")
        return None

def insert_activities(connection, activities):
    cursor = connection.cursor()
    
    for activity in activities:
        cursor.execute("""
        INSERT OR REPLACE INTO activities 
        (key, activity, type, participants, price, link, accessibility)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            activity['key'],
            activity['activity'],
            activity['type'],
            activity['participants'],
            activity['price'],
            activity['link'],
            activity['accessibility']
        ))
    
    connection.commit()

def initialize_system():
    connection = create_database()
    if connection:
        print("Coletando atividades...")
        activities = get_activities(limit=100)
        
        insert_activities(connection, activities)
        print(f"Coletadas e salvas {len(activities)} atividades no banco de dados")
        
        connection.close()
    else:
        print("Falha ao inicializar o sistema")

if __name__ == "__main__":
    initialize_system()
    