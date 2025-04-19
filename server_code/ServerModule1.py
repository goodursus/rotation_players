import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

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
    return bool(os.getenv("ANVIL_APP_SERVER"))


