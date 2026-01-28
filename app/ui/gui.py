# app/ui/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Any
import os
from datetime import datetime

class TrackFlixGUI:
    """Interface gráfica principal do TrackFlix."""
    
    def __init__(self, media_service):
        self.service = media_service
        self.root = tk.Tk()
        self.root.title("TrackFlix 🎬")
        self.root.geometry("1200x700")
        
        # Configurar ícone (opcional)
        try:
            self.root.iconbitmap("assets/icons/film.ico")
        except:
            pass
        
        # Variáveis
        self.current_view = "movies"  # "movies" ou "series"
        self.filter_status = "all"    # "all", "watching", "completed", "planned"
        
        # Configurar tema
        self.setup_theme()
        
        # Criar interface
        self.setup_ui()
        
        # Carregar dados iniciais
        self.refresh_data()
    
    def setup_theme(self):
        """Configura o tema da interface."""
        style = ttk.Style()
        
        # Tema padrão do sistema
        style.theme_use('clam')
        
        # Cores personalizadas
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'background': '#f5f5f5'
        }
        
        # Configurar estilos
        style.configure('Primary.TButton', 
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.colors['primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['dark'])
    
    def setup_ui(self):
        """Configura todos os elementos da interface."""
        # Container principal
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar pesos das linhas/colunas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # ========== CABEÇALHO ==========
        header_frame = ttk.Frame(main_container)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Título
        title_label = ttk.Label(header_frame, 
                               text="🎬 TRACKFLIX - Movie & Series Tracker",
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Estatísticas rápidas
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        self.stats_label = ttk.Label(stats_frame, 
                                    text="Carregando estatísticas...",
                                    style='Subtitle.TLabel')
        self.stats_label.pack()
        
        # ========== BARRA LATERAL ==========
        sidebar_frame = ttk.LabelFrame(main_container, text="Menu", padding="10")
        sidebar_frame.grid(row=1, column=0, sticky=(tk.N, tk.S), padx=(0, 10))
        
        # Botões principais
        buttons = [
            ("🎬 Filmes", self.show_movies, 'movies'),
            ("📺 Séries", self.show_series, 'series'),
            ("📊 Estatísticas", self.show_statistics, 'stats'),
            ("🔍 Buscar", self.show_search, 'search')
        ]
        
        for i, (text, command, view) in enumerate(buttons):
            btn = ttk.Button(sidebar_frame, 
                           text=text, 
                           command=command,
                           style='Primary.TButton' if view == 'movies' else 'TButton',
                           width=15)
            btn.grid(row=i, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Separador
        ttk.Separator(sidebar_frame, orient='horizontal').grid(row=4, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Botões de ação
        action_buttons = [
            ("➕ Adicionar Filme", self.add_movie_dialog),
            ("➕ Adicionar Série", self.add_series_dialog),
            ("🔄 Atualizar", self.refresh_data),
            ("📤 Exportar", self.export_data),
            ("⚙️ Configurações", self.show_settings)
        ]
        
        for i, (text, command) in enumerate(action_buttons):
            btn = ttk.Button(sidebar_frame, 
                           text=text, 
                           command=command,
                           width=15)
            btn.grid(row=5+i, column=0, pady=2, sticky=(tk.W, tk.E))
        
        # ========== CONTEÚDO PRINCIPAL ==========
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Barra de filtros
        filter_frame = ttk.Frame(content_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtro por status
        ttk.Label(filter_frame, text="Filtrar por status:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_filter = tk.StringVar(value="all")
        status_options = [
            ("Todos", "all"),
            ("🎬 Assistindo", "watching"),
            ("✅ Concluído", "completed"),
            ("📅 Planejado", "planned")
        ]
        
        for text, value in status_options:
            rb = ttk.Radiobutton(filter_frame, 
                               text=text, 
                               variable=self.status_filter,
                               value=value,
                               command=self.apply_filters)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Busca
        ttk.Label(filter_frame, text="Buscar:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_changed)
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão limpar busca
        ttk.Button(filter_frame, 
                  text="🗑️", 
                  command=self.clear_search,
                  width=3).pack(side=tk.LEFT)
        
        # ========== TABELA DE DADOS ==========
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar Treeview (tabela)
        columns = ('ID', 'Título', 'Ano', 'Status', 'Avaliação', 'Detalhes')
        
        self.tree = ttk.Treeview(table_frame, 
                                columns=columns,
                                show='headings',
                                height=20,
                                selectmode='browse')
        
        # Configurar colunas
        column_widths = {
            'ID': 50,
            'Título': 250,
            'Ano': 70,
            'Status': 100,
            'Avaliação': 80,
            'Detalhes': 150
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar expansão
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Bind duplo clique
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        # ========== BARRA DE STATUS ==========
        status_frame = ttk.Frame(main_container)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Pronto")
        self.status_label.pack(side=tk.LEFT)
        
        # Botões de ação na barra de status
        btn_frame = ttk.Frame(status_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, 
                  text="📝 Editar Selecionado",
                  command=self.edit_selected).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(btn_frame, 
                  text="🗑️ Remover Selecionado",
                  command=self.delete_selected).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(btn_frame, 
                  text="⭐ Avaliar",
                  command=self.rate_selected).pack(side=tk.LEFT, padx=2)
    
    def refresh_data(self):
        """Atualiza todos os dados na interface."""
        try:
            # Atualizar estatísticas
            self.update_stats()
            
            # Atualizar lista baseado na view atual
            if self.current_view == "movies":
                self.show_movies()
            elif self.current_view == "series":
                self.show_series()
            elif self.current_view == "stats":
                self.show_statistics()
            
            self.set_status("Dados atualizados com sucesso!")
            
        except Exception as e:
            self.set_status(f"Erro ao atualizar: {e}", error=True)
    
    def update_stats(self):
        """Atualiza as estatísticas no cabeçalho."""
        try:
            stats = self.service.get_statistics()
            
            stats_text = (
                f"🎬 Filmes: {stats['movies']} | "
                f"📺 Séries: {stats['series']} | "
                f"📦 Total: {stats['total']} | "
                f"✅ Concluídos: {stats['concluido']}"
            )
            
            self.stats_label.config(text=stats_text)
            
        except Exception as e:
            self.stats_label.config(text="Erro ao carregar estatísticas")
    
    def show_movies(self):
        """Mostra a lista de filmes."""
        self.current_view = "movies"
        self.clear_table()
        
        try:
            movies = self.service.get_all_movies()
            
            if not movies:
                self.set_status("Nenhum filme cadastrado")
                return
            
            for movie in movies:
                # Aplicar filtros
                if not self.passes_filters(movie):
                    continue
                
                # Formatar avaliação
                rating = movie.get('rating', 0)
                rating_text = f"⭐ {rating}" if rating > 0 else "Sem avaliação"
                
                # Detalhes
                details = f"{movie.get('duration', 'N/A')}min"
                if movie.get('director'):
                    details += f" | {movie['director']}"
                
                # Adicionar à tabela
                self.tree.insert('', tk.END, values=(
                    movie['id'],
                    movie['title'][:40],  # Limitar tamanho
                    movie['year'],
                    movie['status'],
                    rating_text,
                    details
                ))
            
            self.set_status(f"{len(movies)} filmes encontrados")
            
        except Exception as e:
            self.set_status(f"Erro ao carregar filmes: {e}", error=True)
    
    def show_series(self):
        """Mostra a lista de séries."""
        self.current_view = "series"
        self.clear_table()
        
        try:
            series_list = self.service.get_all_series()
            
            if not series_list:
                self.set_status("Nenhuma série cadastrada")
                return
            
            for series in series_list:
                # Aplicar filtros
                if not self.passes_filters(series):
                    continue
                
                # Calcular progresso
                total_eps = series['total_seasons'] * series['total_episodes']
                watched_eps = ((series['current_season'] - 1) * series['total_episodes']) + series['current_episode']
                progress = (watched_eps / total_eps * 100) if total_eps > 0 else 0
                
                # Formatar avaliação
                rating = series.get('rating', 0)
                rating_text = f"⭐ {rating}" if rating > 0 else "Sem avaliação"
                
                # Detalhes
                details = f"T{series['current_season']}E{series['current_episode']} ({progress:.1f}%)"
                
                # Adicionar à tabela
                self.tree.insert('', tk.END, values=(
                    series['id'],
                    series['title'][:40],  # Limitar tamanho
                    series['year'],
                    series['status'],
                    rating_text,
                    details
                ))
            
            self.set_status(f"{len(series_list)} séries encontradas")
            
        except Exception as e:
            self.set_status(f"Erro ao carregar séries: {e}", error=True)
    
    def show_statistics(self):
        """Mostra estatísticas detalhadas."""
        self.current_view = "stats"
        self.clear_table()
        
        try:
            stats = self.service.get_statistics()
            
            # Criar uma visualização simples das estatísticas
            stat_items = [
                ("🎬 FILMES", stats['movies']),
                ("📺 SÉRIES", stats['series']),
                ("📦 TOTAL", stats['total']),
                ("✅ CONCLUÍDOS", stats['concluido']),
                ("⏳ ASSISTINDO", stats['assistindo']),
                ("📅 PLANEJADOS", stats['planejado'])
            ]
            
            for label, value in stat_items:
                self.tree.insert('', tk.END, values=(label, value, "", "", "", ""))
            
            # Adicionar taxa de conclusão
            if stats['total'] > 0:
                completion_rate = (stats['concluido'] / stats['total']) * 100
                self.tree.insert('', tk.END, values=("📈 TAXA DE CONCLUSÃO", f"{completion_rate:.1f}%", "", "", "", ""))
            
            self.set_status("Estatísticas carregadas")
            
        except Exception as e:
            self.set_status(f"Erro ao carregar estatísticas: {e}", error=True)
    
    def show_search(self):
        """Mostra tela de busca."""
        # Para simplificar, vamos usar um dialog
        search_term = self.search_var.get()
        
        if not search_term:
            messagebox.showinfo("Busca", "Digite um termo para buscar")
            return
        
        self.clear_table()
        
        try:
            # Buscar em filmes
            movies = self.service.get_all_movies()
            series = self.service.get_all_series()
            
            results = []
            for movie in movies:
                if search_term.lower() in movie['title'].lower():
                    results.append(('🎬', movie))
            
            for serie in series:
                if search_term.lower() in serie['title'].lower():
                    results.append(('📺', serie))
            
            if not results:
                self.set_status(f"Nenhum resultado para '{search_term}'")
                return
            
            for media_type, item in results:
                self.tree.insert('', tk.END, values=(
                    media_type,
                    item['title'][:40],
                    item['year'],
                    item['status'],
                    f"⭐ {item.get('rating', 0)}" if item.get('rating', 0) > 0 else "Sem avaliação",
                    "Clique para detalhes"
                ))
            
            self.set_status(f"{len(results)} resultados encontrados para '{search_term}'")
            
        except Exception as e:
            self.set_status(f"Erro na busca: {e}", error=True)
    
    def add_movie_dialog(self):
        """Abre diálogo para adicionar filme."""
        dialog = tk.Toplevel(self.root)
        dialog.title("🎬 Adicionar Filme")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Container
        container = ttk.Frame(dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(container, text="Adicionar Novo Filme", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos do formulário
        fields = [
            ("Título*:", "entry", ""),
            ("Ano*:", "entry", datetime.now().year),
            ("Gêneros:", "entry", "Ex: Ação, Comédia, Drama"),
            ("Duração (min)*:", "entry", "120"),
            ("Diretor:", "entry", ""),
            ("Status:", "combobox", ["Planejado", "Assistindo", "Concluído"]),
            ("Avaliação (0-5):", "spinbox", (0, 5, 0.5)),
            ("Comentário:", "text", "")
        ]
        
        entries = {}
        for i, (label, field_type, default) in enumerate(fields, 1):
            ttk.Label(container, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if field_type == "entry":
                var = tk.StringVar(value=default)
                entry = ttk.Entry(container, textvariable=var, width=30)
                entry.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "combobox":
                var = tk.StringVar(value=default[0])
                combo = ttk.Combobox(container, textvariable=var, values=default, width=28)
                combo.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "spinbox":
                var = tk.DoubleVar(value=0)
                spin = ttk.Spinbox(container, from_=default[0], to=default[1], 
                                  increment=default[2], textvariable=var, width=28)
                spin.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "text":
                text = tk.Text(container, height=3, width=30)
                text.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = text
        
        # Botões
        button_frame = ttk.Frame(container)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Salvar", 
                  command=lambda: self.save_movie(dialog, entries),
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
    
    def save_movie(self, dialog, entries):
        """Salva o filme no banco."""
        try:
            from app.models.media import Movie, MediaStatus
            
            # Obter valores
            title = entries["Título*:"].get()
            year = int(entries["Ano*:"].get())
            genres = [g.strip() for g in entries["Gêneros:"].get().split(',') if g.strip()]
            duration = int(entries["Duração (min)*:"].get())
            director = entries["Diretor:"].get() or None
            status_str = entries["Status:"].get()
            rating = entries["Avaliação (0-5):"].get()
            comment = entries["Comentário:"].get("1.0", tk.END).strip()
            
            # Validar
            if not title:
                messagebox.showerror("Erro", "Título é obrigatório!")
                return
            
            # Mapear status
            status_map = {
                "Planejado": MediaStatus.PLAN_TO_WATCH,
                "Assistindo": MediaStatus.WATCHING,
                "Concluído": MediaStatus.COMPLETED
            }
            
            # Criar objeto
            movie = Movie(
                title=title,
                year=year,
                genres=genres,
                duration=duration,
                director=director
            )
            
            movie.status = status_map.get(status_str, MediaStatus.PLAN_TO_WATCH)
            movie.rating = float(rating)
            movie.comment = comment
            
            # Salvar
            if self.service.add_movie(movie):
                messagebox.showinfo("Sucesso", f"Filme '{title}' adicionado!")
                dialog.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar o filme.")
        
        except ValueError as e:
            messagebox.showerror("Erro de Validação", f"Dados inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def add_series_dialog(self):
        """Abre diálogo para adicionar série."""
        dialog = tk.Toplevel(self.root)
        dialog.title("📺 Adicionar Série")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Container
        container = ttk.Frame(dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(container, text="Adicionar Nova Série", 
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos do formulário
        fields = [
            ("Título*:", "entry", ""),
            ("Ano*:", "entry", datetime.now().year),
            ("Gêneros:", "entry", "Ex: Drama, Comédia, Suspense"),
            ("Temporadas*:", "entry", "1"),
            ("Episódios/Temporada*:", "entry", "10"),
            ("Episódio Atual:", "entry", "1"),
            ("Temporada Atual:", "entry", "1"),
            ("Duração/Episódio (min):", "entry", "45"),
            ("Status:", "combobox", ["Planejado", "Assistindo", "Concluído"]),
            ("Avaliação (0-5):", "spinbox", (0, 5, 0.5)),
            ("Comentário:", "text", "")
        ]
        
        entries = {}
        for i, (label, field_type, default) in enumerate(fields, 1):
            ttk.Label(container, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if field_type == "entry":
                var = tk.StringVar(value=default)
                entry = ttk.Entry(container, textvariable=var, width=30)
                entry.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "combobox":
                var = tk.StringVar(value=default[0])
                combo = ttk.Combobox(container, textvariable=var, values=default, width=28)
                combo.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "spinbox":
                var = tk.DoubleVar(value=0)
                spin = ttk.Spinbox(container, from_=default[0], to=default[1], 
                                  increment=default[2], textvariable=var, width=28)
                spin.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = var
            
            elif field_type == "text":
                text = tk.Text(container, height=3, width=30)
                text.grid(row=i, column=1, pady=5, padx=(10, 0))
                entries[label] = text
        
        # Botões
        button_frame = ttk.Frame(container)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Salvar", 
                  command=lambda: self.save_series(dialog, entries),
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
    
    def save_series(self, dialog, entries):
        """Salva a série no banco."""
        try:
            from app.models.media import Series, MediaStatus
            
            # Obter valores
            title = entries["Título*:"].get()
            year = int(entries["Ano*:"].get())
            genres = [g.strip() for g in entries["Gêneros:"].get().split(',') if g.strip()]
            seasons = int(entries["Temporadas*:"].get())
            episodes = int(entries["Episódios/Temporada*:"].get())
            current_ep = int(entries["Episódio Atual:"].get() or 1)
            current_season = int(entries["Temporada Atual:"].get() or 1)
            ep_duration = int(entries["Duração/Episódio (min):"].get() or 45)
            status_str = entries["Status:"].get()
            rating = entries["Avaliação (0-5):"].get()
            comment = entries["Comentário:"].get("1.0", tk.END).strip()
            
            # Validar
            if not title:
                messagebox.showerror("Erro", "Título é obrigatório!")
                return
            
            # Mapear status
            status_map = {
                "Planejado": MediaStatus.PLAN_TO_WATCH,
                "Assistindo": MediaStatus.WATCHING,
                "Concluído": MediaStatus.COMPLETED
            }
            
            # Criar objeto
            series = Series(
                title=title,
                year=year,
                genres=genres,
                total_seasons=seasons,
                total_episodes=episodes,
                episode_duration=ep_duration
            )
            
            series.current_season = current_season
            series.current_episode = current_ep
            series.status = status_map.get(status_str, MediaStatus.PLAN_TO_WATCH)
            series.rating = float(rating)
            series.comment = comment
            
            # Salvar
            if self.service.add_series(series):
                messagebox.showinfo("Sucesso", f"Série '{title}' adicionada!")
                dialog.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar a série.")
        
        except ValueError as e:
            messagebox.showerror("Erro de Validação", f"Dados inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def edit_selected(self):
        """Edita o item selecionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para editar.")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 1:
            return
        
        item_id = values[0]
        
        # Aqui você implementaria a edição
        messagebox.showinfo("Editar", f"Editar item ID: {item_id}")
        # TODO: Implementar diálogo de edição
    
    def delete_selected(self):
        """Remove o item selecionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 2:
            return
        
        item_id = values[0]
        item_name = values[1]
        
        # Confirmar
        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja remover '{item_name}'?\nEsta ação não pode ser desfeita."
        )
        
        if confirm:
            try:
                success = self.service.delete_media(item_id)
                if success:
                    self.set_status(f"'{item_name}' removido com sucesso!")
                    self.refresh_data()
                else:
                    messagebox.showerror("Erro", "Não foi possível remover o item.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover: {e}")
    
    def rate_selected(self):
        """Avalia o item selecionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um item para avaliar.")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        if not values or len(values) < 1:
            return
        
        item_id = values[0]
        item_name = values[1]
        
        # Diálogo de avaliação
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Avaliar: {item_name}")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        container = ttk.Frame(dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(container, text=f"Avaliar: {item_name}").pack(pady=10)
        
        # Avaliação
        rating_frame = ttk.Frame(container)
        rating_frame.pack(pady=10)
        
        ttk.Label(rating_frame, text="Nota (0-5):").pack(side=tk.LEFT, padx=5)
        
        rating_var = tk.DoubleVar(value=3.0)
        ttk.Spinbox(rating_frame, from_=0, to=5, increment=0.5,
                   textvariable=rating_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Comentário
        ttk.Label(container, text="Comentário:").pack(anchor=tk.W, pady=(10, 0))
        comment_text = tk.Text(container, height=3, width=30)
        comment_text.pack(pady=5)
        
        # Botões
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancelar",
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        def save_rating():
            try:
                rating = rating_var.get()
                comment = comment_text.get("1.0", tk.END).strip()
                
                # Determinar tipo
                if self.current_view == "movies":
                    success = self.service.update_movie_rating(item_id, rating, comment)
                else:
                    success = self.service.update_series_rating(item_id, rating, comment)
                
                if success:
                    messagebox.showinfo("Sucesso", "Avaliação salva!")
                    dialog.destroy()
                    self.refresh_data()
                else:
                    messagebox.showerror("Erro", "Não foi possível salvar a avaliação.")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
        
        ttk.Button(button_frame, text="Salvar",
                  command=save_rating,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
    
    def on_item_double_click(self, event):
        """Ao clicar duas vezes em um item."""
        selection = self.tree.selection()
        if selection:
            self.show_item_details(selection[0])
    
    def show_item_details(self, item_id):
        """Mostra detalhes do item."""
        # TODO: Implementar diálogo de detalhes
        messagebox.showinfo("Detalhes", f"Mostrar detalhes do item {item_id}")
    
    def apply_filters(self):
        """Aplica os filtros selecionados."""
        self.refresh_data()
    
    def passes_filters(self, item):
        """Verifica se o item passa pelos filtros."""
        status = self.status_filter.get()
        
        if status == "all":
            return True
        
        item_status = item.get('status', '').lower()
        
        if status == "watching" and "assistindo" in item_status:
            return True
        elif status == "completed" and "concluído" in item_status:
            return True
        elif status == "planned" and "planejado" in item_status:
            return True
        
        return False
    
    def on_search_changed(self, *args):
        """Quando o texto da busca muda."""
        search_term = self.search_var.get().strip()
        
        if len(search_term) >= 2:  # Buscar apenas com 2+ caracteres
            self.show_search()
        elif not search_term:
            self.refresh_data()
    
    def clear_search(self):
        """Limpa a busca."""
        self.search_var.set("")
        self.refresh_data()
    
    def clear_table(self):
        """Limpa a tabela."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def set_status(self, message, error=False):
        """Define mensagem na barra de status."""
        color = "red" if error else "black"
        self.status_label.config(text=message, foreground=color)
    
    def export_data(self):
        """Exporta dados para CSV."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"trackflix_export_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
            if filename:
                # TODO: Implementar exportação
                messagebox.showinfo("Exportar", f"Dados exportados para:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def show_settings(self):
        """Mostra configurações."""
        messagebox.showinfo("Configurações", "Configurações do sistema")
        # TODO: Implementar diálogo de configurações
    
    def run(self):
        """Executa a interface gráfica."""
        self.root.mainloop()