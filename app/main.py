# app/main.py
from app.database.db import Database
from app.services.media_service import MediaService

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
        
        # Perguntar qual interface usar
        print("\n" + "=" * 70)
        print("📱 Selecione o modo de interface:")
        print("1. 🖥️  Interface Gráfica (GUI)")
        print("2. 💻 Interface de Linha de Comando (CLI)")
        print("=" * 70)
        
        choice = input("\n👉 Escolha (1 ou 2): ").strip()
        
        if choice == "1":
            # Executar GUI
            from app.ui.gui import TrackFlixGUI
            print("\n🎨 Iniciando interface gráfica...")
            gui = TrackFlixGUI(media_service)
            gui.run()
        else:
            # Executar CLI
            from app.ui.cli import CLI
            print("\n💻 Iniciando interface de linha de comando...")
            cli = CLI(media_service)
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