# run.py (na raiz do projeto)
import sys
import os

# Adicionar o diretório atual ao path do Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Iniciando TrackFlix...")

try:
    from app.main import main
    print("✅ Módulos carregados com sucesso!")
    print("=" * 70)
    main()
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n📁 Verificando estrutura...")
    
    # Verificar arquivos
    if not os.path.exists('app'):
        print("❌ Pasta 'app' não encontrada!")
    else:
        print("📁 Conteúdo de 'app':")
        for item in os.listdir('app'):
            print(f"  - {item}")
            
            if os.path.isdir(os.path.join('app', item)):
                subpath = os.path.join('app', item)
                for subitem in os.listdir(subpath):
                    print(f"    - {subitem}")
    
    input("\n👆 Pressione Enter para sair...")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    input("\n👆 Pressione Enter para sair...")