import sqlite3

conn = sqlite3.connect('trackflix.db')
cursor = conn.cursor()

# Adicionar coluna media_id
cursor.execute("ALTER TABLE movies ADD COLUMN media_id INTEGER")
conn.commit()
conn.close()

print("Coluna media_id adicionada com sucesso!")