# app/database/db.py
import sqlite3
from datetime import datetime

class Database:
    """Gerencia conexões com o banco de dados SQLite."""
    
    def __init__(self, db_path="trackflix.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados criando as tabelas."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de mídias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                genres TEXT,
                rating REAL DEFAULT 0,
                comment TEXT,
                status TEXT DEFAULT 'Planejado',
                media_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de filmes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                media_id INTEGER PRIMARY KEY,
                duration INTEGER,
                director TEXT,
                watched_date TIMESTAMP,
                FOREIGN KEY (media_id) REFERENCES media(id)
            )
        ''')
        
        # Tabela de séries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS series (
                media_id INTEGER PRIMARY KEY,
                total_seasons INTEGER,
                total_episodes INTEGER,
                current_season INTEGER DEFAULT 1,
                current_episode INTEGER DEFAULT 1,
                episode_duration INTEGER,
                FOREIGN KEY (media_id) REFERENCES media(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado!")
    
    def get_connection(self):
        """Retorna uma conexão com o banco."""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()):
        """Executa uma query e retorna o cursor."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor
    
    def fetch_all(self, query: str, params: tuple = ()):
        """Executa uma query e retorna todos os resultados."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def fetch_one(self, query: str, params: tuple = ()):
        """Executa uma query e retorna um resultado."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result