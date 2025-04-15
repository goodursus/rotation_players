import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import csv

@anvil.server.callable
def import_data_from_csv():

    print("Функция import_data_from_csv вызвана!")

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
