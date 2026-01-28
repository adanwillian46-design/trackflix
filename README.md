# 🎬 TrackFlix - Movie & Series Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

Aplicação desktop em Python para gerenciamento pessoal de filmes e séries com banco de dados SQLite.

## ✨ Demonstração

![TrackFlix Demo](demo.gif) *Adicione um GIF mostrando o funcionamento*

## 🚀 Funcionalidades

- ✅ **Cadastro completo** de filmes e séries
- ✅ **Controle de progresso** com porcentagem
- ✅ **Sistema de avaliação** (0-5 estrelas)
- ✅ **Estatísticas detalhadas** do acervo
- ✅ **Busca inteligente** por título
- ✅ **Interface CLI** intuitiva e colorida
- ✅ **Persistência** com SQLite
- ✅ **Validações** robustas de dados

## 🛠 Tecnologias

- **Python 3.10+** - Linguagem principal
- **SQLite** - Banco de dados embutido
- **POO** - Programação Orientada a Objetos
- **MVC** - Arquitetura Model-View-Controller
- **SQL** - Consultas diretas ao banco

## 📁 Estrutura do Projeto
trackflix/
- ├── app/
- │ ├── models/ # 🎭 Classes Movie e Series
- │ ├── database/ # 💾 Gerenciamento SQLite
- │ ├── services/ # ⚙️ Lógica de negócio
- │ └── ui/ # 🖥️ Interface CLI
- ├── tests/ # 🧪 Testes automatizados
- ├── requirements.txt # 📦 Dependências
- └── README.md # 📚 Documentação



## ⚡ Como Executar

```bash
# Clone o repositório
git clone https://github.com/seuusuario/trackflix.git
cd trackflix

# Execute (não precisa de instalação)
python run.py

# Ou
python -m app.main

🎯 Exemplo de Uso
python
# Exemplo de código
from app.models.media import Movie

# Criar um filme
movie = Movie("Inception", 2010, ["Sci-Fi", "Thriller"], 148, "Christopher Nolan")
print(movie)  # 🎬 Inception (2010) - 148min



