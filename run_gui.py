# run_gui.py (executar apenas GUI)
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Iniciando TrackFlix GUI...")

try:
    from app.database.db import Database
    from app.services.media_service import MediaService
    from app.ui.gui import TrackFlixGUI
    
    db = Database()
    service = MediaService(db)
    app = TrackFlixGUI(service)
    app.run()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione Enter para sair...")