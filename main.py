# app/main.py
from app.database.db import Database
from app.services.media_service import MediaService
from app.ui.cli import CLI

def main():
    """Ponto de entrada principal da aplicação."""
    print("\n" + "=" * 70)
    print("🎬 TRACKFLIX - Movie & Series Tracker")
    print("=" * 70)
    print("🚀 Sistema inicializando...")
    
    try:
        # Inicializar componentes
        db = Database()
        media_service = MediaService(db)
        cli = CLI(media_service)
        
        print("✅ Sistema pronto!")
        print("=" * 70 + "\n")
        
        input("👆 Pressione Enter para começar...")
        
        # Executar interface
        cli.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n💥 ERRO: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()