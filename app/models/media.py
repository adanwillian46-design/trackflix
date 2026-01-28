# app/models/media.py
from datetime import datetime
from typing import List, Optional
from enum import Enum

class MediaType(Enum):
    MOVIE = "movie"
    SERIES = "series"

class MediaStatus(Enum):
    PLAN_TO_WATCH = "Planejado"
    WATCHING = "Assistindo"
    COMPLETED = "Concluído"

class Media:
    """Classe base para todas as mídias."""
    
    def __init__(self, title: str, year: int, genres: List[str]):
        self.title = title
        self.year = year
        self.genres = genres
        self.rating = 0.0
        self.comment = ""
        self.status = MediaStatus.PLAN_TO_WATCH
        self.created_at = datetime.now()
        self.type = None  # Será definido nas subclasses
    
    def validate(self):
        """Valida os dados da mídia."""
        if not self.title.strip():
            raise ValueError("Título não pode ser vazio")
        if self.year < 1888 or self.year > datetime.now().year + 2:
            raise ValueError(f"Ano inválido: {self.year}")
        if self.rating < 0 or self.rating > 5:
            raise ValueError("Avaliação deve ser entre 0 e 5")
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class Movie(Media):
    """Classe para filmes."""
    
    def __init__(self, title: str, year: int, genres: List[str], 
                 duration: int, director: Optional[str] = None):
        super().__init__(title, year, genres)
        self.duration = duration
        self.director = director
        self.watched_date = None
        self.type = MediaType.MOVIE
    
    def mark_as_watched(self):
        """Marca o filme como assistido."""
        self.status = MediaStatus.COMPLETED
        self.watched_date = datetime.now()
    
    def __str__(self):
        return f"🎬 {self.title} ({self.year}) - {self.duration}min"

class Series(Media):
    """Classe para séries."""
    
    def __init__(self, title: str, year: int, genres: List[str],
                 total_seasons: int, total_episodes: int,
                 episode_duration: Optional[int] = None):
        super().__init__(title, year, genres)
        self.total_seasons = total_seasons
        self.total_episodes = total_episodes
        self.episode_duration = episode_duration
        self.current_season = 1
        self.current_episode = 1
        self.type = MediaType.SERIES
    
    @property
    def progress_percentage(self):
        """Calcula o progresso em porcentagem."""
        total = self.total_seasons * self.total_episodes
        if total == 0:
            return 0
        watched = ((self.current_season - 1) * self.total_episodes) + self.current_episode
        return round((watched / total) * 100, 2)
    
    def update_progress(self, season: int, episode: int):
        """Atualiza o progresso da série."""
        if 1 <= season <= self.total_seasons and 1 <= episode <= self.total_episodes:
            self.current_season = season
            self.current_episode = episode
            
            if self.progress_percentage == 100:
                self.status = MediaStatus.COMPLETED
            elif self.progress_percentage > 0:
                self.status = MediaStatus.WATCHING
    
    def __str__(self):
        return f"📺 {self.title} ({self.year}) - T{self.current_season}E{self.current_episode}"