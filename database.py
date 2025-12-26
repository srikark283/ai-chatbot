import sqlite3
from datetime import datetime
from typing import List, Dict

class ChatDatabase:
    """SQLite database handler for storing chat sessions and history."""
    
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sessions table with title support
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        conn.commit()
        conn.close()

    def create_session(self, session_id: str, title: str = "New Chat") -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO sessions (session_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (session_id, title, datetime.now(), datetime.now()))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def update_session_title(self, session_id: str, title: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET title = ? WHERE session_id = ?", (title, session_id))
        conn.commit()
        conn.close()

    def add_message(self, session_id: str, role: str, content: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE sessions SET updated_at = ? WHERE session_id = ?", (datetime.now(), session_id))
        cursor.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
        conn.commit()
        conn.close()
        return True

    def get_session_history(self, session_id: str) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"role": row[0], "content": row[1]} for row in rows]

    def get_all_sessions(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT session_id, title FROM sessions ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"session_id": r[0], "title": r[1]} for r in rows]

    def delete_session(self, session_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()