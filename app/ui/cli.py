# app/ui/cli.py
import os
from typing import Optional
from app.services.media_service import MediaService
from app.models.media import Movie, Series

class CLI:
    """Interface de linha de comando."""
    
    def __init__(self, media_service: MediaService):
        self.service = media_service
        self.running = True
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        self.clear_screen()
        print("=" * 60)
        print(f"🎬 {title}")
        print("=" * 60)
        print()
    
    def wait_for_enter(self):
        input("\n👆 Pressione Enter para continuar...")
    
    def get_input(self, prompt: str, default: str = "") -> str:
        if default:
            full_prompt = f"{prompt} [{default}]: "
        else:
            full_prompt = f"{prompt}: "
        
        value = input(full_prompt).strip()
        return value if value else default
    
    def get_int_input(self, prompt: str, default: int = 0,
                      min_val: Optional[int] = None,
                      max_val: Optional[int] = None) -> int:
        while True:
            try:
                value = self.get_input(prompt, str(default) if default != 0 else "")
                if not value and default is not None:
                    return default
                
                num = int(value)
                
                if min_val is not None and num < min_val:
                    print(f"❌ Valor deve ser ≥ {min_val}")
                    continue
                
                if max_val is not None and num > max_val:
                    print(f"❌ Valor deve ser ≤ {max_val}")
                    continue
                
                return num
            except ValueError:
                print("❌ Por favor, digite um número válido")
    
    def add_movie(self):
        """Menu para adicionar filme."""
        self.print_header("ADICIONAR FILME")
        
        print("📝 Preencha os dados do filme:")
        print("-" * 40)
        
        title = self.get_input("Título")
        if not title:
            print("❌ Título é obrigatório!")
            self.wait_for_enter()
            return
        
        year = self.get_int_input("Ano de lançamento", 2024, 1888, 2030)
        
        genres_input = self.get_input("Gêneros (separados por vírgula)")
        genres = [g.strip() for g in genres_input.split(',') if g.strip()]
        
        duration = self.get_int_input("Duração (minutos)", 120, 1, 500)
        director = self.get_input("Diretor (opcional)")
        
        # Criar objeto Movie
        movie = Movie(
            title=title,
            year=year,
            genres=genres,
            duration=duration,
            director=director if director else None
        )
        
        # Salvar
        if self.service.add_movie(movie):
            print(f"\n✅ Filme '{title}' adicionado com sucesso!")
        else:
            print("\n❌ Erro ao adicionar filme")
        
        self.wait_for_enter()
    
    def add_series(self):
        """Menu para adicionar série."""
        self.print_header("ADICIONAR SÉRIE")
        
        print("📝 Preencha os dados da série:")
        print("-" * 40)
        
        title = self.get_input("Título")
        if not title:
            print("❌ Título é obrigatório!")
            self.wait_for_enter()
            return
        
        year = self.get_int_input("Ano de lançamento", 2024, 1888, 2030)
        
        genres_input = self.get_input("Gêneros (separados por vírgula)")
        genres = [g.strip() for g in genres_input.split(',') if g.strip()]
        
        seasons = self.get_int_input("Número de temporadas", 1, 1, 50)
        episodes = self.get_int_input("Episódios por temporada", 10, 1, 100)
        episode_duration = self.get_int_input("Duração por episódio (minutos, opcional)", 45, 1, 180)
        
        # Criar objeto Series
        series = Series(
            title=title,
            year=year,
            genres=genres,
            total_seasons=seasons,
            total_episodes=episodes,
            episode_duration=episode_duration
        )
        
        # Salvar
        if self.service.add_series(series):
            print(f"\n✅ Série '{title}' adicionada com sucesso!")
        else:
            print("\n❌ Erro ao adicionar série")
        
        self.wait_for_enter()
    
    def list_movies(self):
        """Lista todos os filmes."""
        self.print_header("MEUS FILMES")
        
        movies = self.service.get_all_movies()
        
        if not movies:
            print("📭 Nenhum filme cadastrado")
            print("\nAdicione seu primeiro filme usando a opção 1!")
        else:
            print(f"🎬 Total: {len(movies)} filme(s)")
            print("-" * 60)
            
            for i, movie in enumerate(movies, 1):
                print(f"\n{i}. {movie['title']} ({movie['year']})")
                if movie['rating'] > 0:
                    print(f"   ⭐ Avaliação: {movie['rating']}/5")
                print(f"   📀 Duração: {movie['duration']} min")
                print(f"   🎭 Gêneros: {movie['genres']}")
                print(f"   📋 Status: {movie['status']}")
                if movie['director']:
                    print(f"   👨‍🎨 Diretor: {movie['director']}")
        
        self.wait_for_enter()
    
    def list_series(self):
        """Lista todas as séries."""
        self.print_header("MINHAS SÉRIES")
        
        series_list = self.service.get_all_series()
        
        if not series_list:
            print("📭 Nenhuma série cadastrada")
            print("\nAdicione sua primeira série usando a opção 2!")
        else:
            print(f"📺 Total: {len(series_list)} série(s)")
            print("-" * 60)
            
            for i, series in enumerate(series_list, 1):
                # Calcular progresso
                total_eps = series['total_seasons'] * series['total_episodes']
                watched_eps = ((series['current_season'] - 1) * series['total_episodes']) + series['current_episode']
                progress = (watched_eps / total_eps * 100) if total_eps > 0 else 0
                
                print(f"\n{i}. {series['title']} ({series['year']})")
                if series['rating'] > 0:
                    print(f"   ⭐ Avaliação: {series['rating']}/5")
                print(f"   📊 Progresso: T{series['current_season']}E{series['current_episode']} ({progress:.1f}%)")
                print(f"   🎭 Gêneros: {series['genres']}")
                print(f"   📋 Status: {series['status']}")
                print(f"   🕒 Temporadas: {series['total_seasons']} × {series['total_episodes']} episódios")
        
        self.wait_for_enter()
    
    def show_statistics(self):
        """Mostra estatísticas."""
        self.print_header("ESTATÍSTICAS")
        
        stats = self.service.get_statistics()
        
        print("📊 RESUMO DO SEU ACERVO")
        print("=" * 40)
        print()
        print(f"🎬 FILMES: {stats['movies']}")
        print(f"📺 SÉRIES: {stats['series']}")
        print(f"📦 TOTAL: {stats['total']}")
        print()
        print(f"✅ CONCLUÍDOS: {stats['concluido']}")
        print(f"⏳ ASSISTINDO: {stats['assistindo']}")
        print(f"📅 PLANEJADOS: {stats['planejado']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['concluido'] / stats['total']) * 100
            print(f"\n📈 TAXA DE CONCLUSÃO: {completion_rate:.1f}%")
        
        print("\n" + "=" * 40)
        print("🎯 Metas de Conclusão:")
        print("• 🥇 Ouro: 70% concluído")
        print("• 🥈 Prata: 50% concluído")
        print("• 🥉 Bronze: 30% concluído")
        
        self.wait_for_enter()
    
    def main_menu(self):
        """Menu principal."""
        while self.running:
            self.print_header("TRACKFLIX - MENU PRINCIPAL")
            
            print("[1] 📥 Adicionar Filme")
            print("[2] 📺 Adicionar Série")
            print("[3] 🎬 Meus Filmes")
            print("[4] 📺 Minhas Séries")
            print("[5] 📊 Estatísticas")
            print("[0] 🚪 Sair")
            print()
            
            try:
                choice = self.get_int_input("Opção", min_val=0, max_val=5)
                
                if choice == 0:
                    self.running = False
                    print("\n👋 Obrigado por usar o TrackFlix! Até logo!\n")
                elif choice == 1:
                    self.add_movie()
                elif choice == 2:
                    self.add_series()
                elif choice == 3:
                    self.list_movies()
                elif choice == 4:
                    self.list_series()
                elif choice == 5:
                    self.show_statistics()
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrompido pelo usuário")
                self.running = False
            except Exception as e:
                print(f"\n❌ Erro: {e}")
                self.wait_for_enter()
    
    def run(self):
        """Executa a aplicação."""
        self.main_menu()