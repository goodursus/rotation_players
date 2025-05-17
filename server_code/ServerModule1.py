import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import json
import csv
import io

try:
    from dotenv import load_dotenv
    import os
    import csv
    from datetime import datetime

    load_dotenv()

    anvil_app_server_flag = os.getenv("ANVIL_APP_SERVER", "False")
    print("ANVIL_APP_SERVER =", anvil_app_server_flag)

except (ImportError, ModuleNotFoundError):
    # we're likely in Anvil cloud
    app_server_flag = "cloud"
    print("Running in Anvil Cloud")

@anvil.server.callable
def add_player(player_data):
  if player_data.get('name'):
      app_tables.players.add_row(**player_data)

@anvil.server.callable
def update_player(player, player_data):
  if player_data['name']:
    player.update(**player_data)

@anvil.server.callable
def delete_player(player):
    player.delete()    

# In your Server Module
@anvil.server.callable
def get_courts():
  # Get a list of articles from the Data Table, sorted by 'created' column, in descending order
  return app_tables.courts.search(
    tables.order_by("id", ascending = True)
  )  

def get_game_status(value):
  color_map = {1: "#d4edda", -1: "#cce5ff", 0: "#fff3cd"}  # Цвет фона
  return color_map.get(value, "#ffffff")

def get_score(value):
  if value < 0:
    score = 0
  else:
    score = value
  return score 

@anvil.server.callable
def get_records_with_names():
    # Создаем словарь кодов и имен
    players_dict = {row['player_number']: row['name'] for row in app_tables.s_players.search()}
    
    # Загружаем записи и подставляем имя + другие данные
    records = [
        {
            "name_1": players_dict.get(row['player_id_1'], "Not attached"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_1": row['player_id_1'],
            "name_2": players_dict.get(row['player_id_2'], "Not attached"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_2": row['player_id_2'],
            "name_3": players_dict.get(row['player_id_3'], "Not attached"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_3": row['player_id_3'],
            "name_4": players_dict.get(row['player_id_4'], "Not attached"),  # Если код отсутствует, ставим "Неизвестно"
            "player_id_4": row['player_id_4'],
            "id": row['id'],  # Дополнительные текстовые поля
            "game_id": row['game_id'],
            "bg_color_1": get_game_status(row['status_1']),
            "status_1": row['status_1'],
            "bg_color_2": get_game_status(row['status_2']),
            "status_2": row['status_2'],
            "bg_color_3": get_game_status(row['status_3']),
            "status_3": row['status_3'],
            "bg_color_4": get_game_status(row['status_4']),
            "status_4": row['status_4'],
            "score_1": get_score(row['status_1']),
            "score_3": get_score(row['status_3'])
        }
        for row in app_tables.courts.search()
    ]
    # *** ОТЛАДОЧНЫЙ ВЫВОД ***
    #for record in records:
    #    print(f"Status: {record['status']}, Bg Color: {record['bg_color']}")
    return records

@anvil.server.callable
def add_session(session_data):
  if session_data.get('session_id') and session_data.get('data_session') and session_data.get('number_players'):
      app_tables.session.add_row(**session_data)

@anvil.server.callable
def update_session(session, session_data):
  if session_data['session_id'] and session_data['data_session'] and session_data['number_players'] and session_data['number_courts']:
    session.update(**session_data)

@anvil.server.callable
def delete_session(session):
    session.delete() 

@anvil.server.callable
def add_s_player(s_player_data):
  if s_player_data.get('player_number') and s_player_data.get('name'):
      app_tables.s_players.add_row(**s_player_data)  

@anvil.server.callable
def delete_s_player(player):
  player.delete()

#  # Получаем все оставшиеся строки, сортируя по id
#  all_rows = sorted(app_tables.s_players.search(), key=lambda row: row['player_number'])

#  # Перенумеровываем id
#  for new_id, row in enumerate(all_rows, start = 1):
#    row['player_number'] = new_id  # Присваиваем новый порядковый номер

@anvil.server.callable
def update_s_player(player, player_data):
  if player_data['player_number'] and player_data['name']:
    player.update(**player_data)

@anvil.server.callable
def add_court(court_data):
  if court_data.get('id') and court_data.get('game_id'):
      app_tables.courts.add_row(**court_data)  

@anvil.server.callable
def add_zero_court(court_data):
  app_tables.courts.add_row(**court_data)  

@anvil.server.callable
def is_local_server():
      
  if anvil_app_server_flag == "False":
      print("✅ LOCAL")
  else:
      print("☁️ CLOUD")    
      
  return bool(anvil_app_server_flag)


@anvil.server.callable
def copy_cloud_to_local():
    
    folder = "data-backup"
    
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            table_name = filename[:-4]  # без ".csv"
            csv_path = os.path.join(folder, filename)

            if not hasattr(app_tables, table_name):
                print(f"⚠️ Table '{table_name}' not find — skeep")
                continue

            table = getattr(app_tables, table_name)
            print(f"🔄 Loading in table: {table_name}")

            # Получаем типы колонок
            col_types = {
                col["name"]: col["type"]
                for col in table.list_columns()
            }

            # Очищаем таблицу
            for row in table.search():
                row.delete()

            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    clean_row = {}
                    for col, value in row.items():
                        if col == "ID":
                            continue  # Anvil сам управляет ID

                        if col not in col_types:
                            continue  # защита от лишнего столбца

                        if value == "":
                            clean_row[col] = None
                        elif col_types[col] == "number":
                            clean_row[col] = float(value) if '.' in value else int(value)
                        elif col_types[col] == "boolean":
                            clean_row[col] = value.strip().lower() in ['true', '1', 'yes']
                        elif col_types[col] == "date":
                            for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"):
                                try:
                                    clean_row[col] = datetime.strptime(value, fmt).date()
                                    break
                                except ValueError:
                                    continue
                            else:
                                raise ValueError(f"Unexepted date format: {value}")
                        else:
                            clean_row[col] = value

                    table.add_row(**clean_row)
                    

            print(f"✅ {table_name}: Loading {reader.line_num - 1} rows")

@anvil.server.callable
def download_players(format):
    rows = app_tables.players.search()
    data = [dict(row) for row in rows]

    if format == 'CSV':
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        else:
            output.write('')
        content = output.getvalue().encode()
        mime = 'text/csv'
        name = 'players.csv'
    else:
        content = json.dumps(data, indent=2).encode()
        mime = 'application/json'
        name = 'players.json'

    return anvil.BlobMedia(mime, content, name=name)

@anvil.server.callable
def delete_all_players():
    rows = app_tables.players.search()
    for row in rows:
        row.delete()  

@anvil.server.callable
def upload_players(file):
    content = file.get_bytes().decode()
    
    if file.content_type == 'application/json' or file.name.endswith('.json'):
        data = json.loads(content)
    elif file.content_type == 'text/csv' or file.name.endswith('.csv'):
        reader = csv.DictReader(io.StringIO(content))
        data = [row for row in reader]
    else:
        raise ValueError("Unsupported file type. Please upload JSON or CSV.")
    
    for item in data:
        item.pop('id', None)  # очистить id если есть
        app_tables.players.add_row(**item)

@anvil.server.callable
def get_session_dropdown_items():
  sessions = app_tables.session.search(open = True)
  items = []
  for s in sessions:
    text = (
      f"Session {s['session_id']} | Date: {s['data_session'].strftime('%Y-%m-%d')} | "
      f"Players: {s['number_players']} | Courts: {s['number_courts']} | "
      f"Session duration: {s['session_duration']} min | Game duration: {s['game_duration']} min"
    )
    # (отображаемый текст, значение)
    items.append((text, s))  # Если значение == текст
#    items.append(text)  # Если значение == текст

  return items

@anvil.server.callable
def replace_players_for_session(session_id, tag_list):
  """
    Полностью заменяет все теги для заданной session_id:
    - удаляет старые строки
    - добавляет новые
    """
  # Удалить все существующие строки с этим session_id
  for row in app_tables.s_players.search(session_id=session_id):
    row.delete()

    # Добавить новые теги
  count = 1  
  for tag in tag_list:
    app_tables.s_players.add_row(session_id = session_id, player_number = count, name = tag) 
    count += 1