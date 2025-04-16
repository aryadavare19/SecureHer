# location_danger_history.py
from db_config import get_db_connection

def get_location_history_text():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query the right table
    cursor.execute("""
        SELECT l.name, d.danger_score, d.last_reported
        FROM location_danger d
        JOIN locations l ON d.location_id = l.id
        ORDER BY d.danger_score DESC, d.last_reported DESC
    """)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    if not result:
        return "⚠️ No danger zones reported yet."
    else:
        history_text = "📍 High-Risk Locations:\n\n"
        for row in result:
            history_text += f"- {row[0]} | Danger Score: {row[1]} | Last Reported: {row[2]}\n"
        return history_text
