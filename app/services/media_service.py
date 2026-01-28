# app/services/media_service.py
from typing import List, Dict, Any
from app.models.media import Movie, Series, MediaStatus
from app.database.db import Database

class MediaService:
    """Serviço para gerenciar operações com mídias."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_movie(self, movie: Movie) -> bool:
        """Adiciona um filme ao banco."""
        try:
            # Primeiro insere na tabela media
            query = '''
                INSERT INTO media (title, year, genres, rating, comment, status, media_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                movie.title,
                movie.year,
                ', '.join(movie.genres),
                movie.rating,
                movie.comment,
                movie.status.value,
                'movie'
            )
            
            cursor = self.db.execute_query(query, params)
            movie_id = cursor.lastrowid
            
            # Depois insere na tabela movies
            query = '''
                INSERT INTO movies (media_id, duration, director, watched_date)
                VALUES (?, ?, ?, ?)
            '''
            params = (
                movie_id,
                movie.duration,
                movie.director,
                movie.watched_date.isoformat() if movie.watched_date else None
            )
            
            self.db.execute_query(query, params)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar filme: {e}")
            return False
    
    def add_series(self, series: Series) -> bool:
        """Adiciona uma série ao banco."""
        try:
            # Primeiro insere na tabela media
            query = '''
                INSERT INTO media (title, year, genres, rating, comment, status, media_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                series.title,
                series.year,
                ', '.join(series.genres),
                series.rating,
                series.comment,
                series.status.value,
                'series'
            )
            
            cursor = self.db.execute_query(query, params)
            series_id = cursor.lastrowid
            
            # Depois insere na tabela series
            query = '''
                INSERT INTO series (media_id, total_seasons, total_episodes, 
                                  current_season, current_episode, episode_duration)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = (
                series_id,
                series.total_seasons,
                series.total_episodes,
                series.current_season,
                series.current_episode,
                series.episode_duration
            )
            
            self.db.execute_query(query, params)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar série: {e}")
            return False
    
    def get_all_movies(self) -> List[Dict[str, Any]]:
        """Retorna todos os filmes."""
        query = '''
            SELECT m.*, mv.duration, mv.director, mv.watched_date
            FROM media m
            JOIN movies mv ON m.id = mv.media_id
            ORDER BY m.title
        '''
        
        rows = self.db.fetch_all(query)
        if not rows:
            return []
        
        # Obter nomes das colunas
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        movies = []
        for row in rows:
            movies.append(dict(zip(columns, row)))
        
        return movies
    
    def get_all_series(self) -> List[Dict[str, Any]]:
        """Retorna todas as séries."""
        query = '''
            SELECT m.*, s.total_seasons, s.total_episodes, 
                   s.current_season, s.current_episode, s.episode_duration
            FROM media m
            JOIN series s ON m.id = s.media_id
            ORDER BY m.title
        '''
        
        rows = self.db.fetch_all(query)
        if not rows:
            return []
        
        # Obter nomes das colunas
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        series_list = []
        for row in rows:
            series_list.append(dict(zip(columns, row)))
        
        return series_list
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema."""
        stats = {}
        
        # Total de filmes
        query = "SELECT COUNT(*) FROM media WHERE media_type = 'movie'"
        result = self.db.fetch_one(query)
        stats['movies'] = result[0] if result else 0
        
        # Total de séries
        query = "SELECT COUNT(*) FROM media WHERE media_type = 'series'"
        result = self.db.fetch_one(query)
        stats['series'] = result[0] if result else 0
        
        # Status
        stats['concluido'] = 0
        stats['assistindo'] = 0
        stats['planejado'] = 0
        
        query = "SELECT status, COUNT(*) FROM media GROUP BY status"
        results = self.db.fetch_all(query)
        for status, count in results:
            if status == 'Concluído':
                stats['concluido'] = count
            elif status == 'Assistindo':
                stats['assistindo'] = count
            elif status == 'Planejado':
                stats['planejado'] = count
        
        stats['total'] = stats['movies'] + stats['series']
        
        return stats