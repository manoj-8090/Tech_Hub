from database import db_session, get_db_connection

class UserModel:
    @staticmethod
    def create(name, email, password_hash, role='User'):
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, role)
            )
            return cursor.lastrowid

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()

    @staticmethod
    def find_by_id(user_id):
        conn = get_db_connection()
        try:
            user = conn.execute(
                "SELECT id, name, email, role, created_at FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()


class HistoryModel:
    @staticmethod
    def add(user_id, query, topic, sources_count):
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO search_history (user_id, query, topic, sources_count) VALUES (?, ?, ?, ?)",
                (user_id, query, topic, sources_count)
            )
            return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id, limit=30):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM search_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


class SavedAnswerModel:
    @staticmethod
    def save(user_id, query_id, source, answer, url, confidence):
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO saved_answers (user_id, query_id, source, answer, url, confidence)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, query_id, source, answer, url, confidence)
            )
            return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM saved_answers WHERE user_id = ? ORDER BY saved_at DESC",
                (user_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()
