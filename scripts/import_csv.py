from anvil.tables import app_tables
import csv

# подключись к локальному серверу
#anvil.server.connect("", quiet=True)  # можно оставить пустым в локальном режиме

#from anvil.tables import app_tables

with open("data-backup/players.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        app_tables.players.add_row(**row)

with open("data-backup/courts.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        app_tables.courts.add_row(**row)

with open("data-backup/s_players.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        app_tables.players.add_row(**row)

with open("data-backup/session.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        app_tables.courts.add_row(**row)


print("Импорт завершён.")
