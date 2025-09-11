import sqlite3
from typing import List, Optional
from contextlib import contextmanager
from models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_username ON users(username)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_email ON users(email)
            """)
    
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def create(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO users (username, email, password_hash, is_active)
                VALUES (?, ?, ?, ?)
            """, (user.username, user.email, user.password_hash, user.is_active))
            
            user.id = cursor.lastrowid
            user.created_at = datetime.now()
            user.updated_at = datetime.now()
            return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            return self._row_to_user(row) if row else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            return self._row_to_user(row) if row else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
            return self._row_to_user(row) if row else None
    
    def update(self, user: User) -> User:
        if not user.id:
            raise ValueError("User ID is required for update")
        
        user.updated_at = datetime.now()
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE users 
                SET username = ?, email = ?, password_hash = ?, 
                    updated_at = ?, is_active = ?
                WHERE id = ?
            """, (user.username, user.email, user.password_hash, 
                  user.updated_at, user.is_active, user.id))
            return user
    
    def delete(self, user_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            ).fetchall()
            return [self._row_to_user(row) for row in rows]
    
    def _row_to_user(self, row) -> User:
        return User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            is_active=bool(row['is_active'])
        )